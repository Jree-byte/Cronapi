import streamlit as st
import mysql.connector
import pandas as pd
import re

# -------------------------
# Streamlit page config
# -------------------------
try:
    st.set_page_config(page_title="Weather & Aviation Data", layout="wide")
except:
    pass  # jos vanha Streamlit-versio ei tue

st.title("Weather & Aviation Data Dashboard")

# -------------------------
# MySQL connection
# -------------------------
try:
    conn = mysql.connector.connect(
        host='localhost',
        user='VITTU',
        password='Moimoi33-',
        database='weather'
    )
except mysql.connector.Error as e:
    st.error(f"Tietokantavirhe: {e}")
    st.stop()

# -------------------------
# WEATHER DATA
# -------------------------
try:
    weather_df = pd.read_sql(
        "SELECT * FROM weather_data ORDER BY timestamp DESC LIMIT 50",
        conn
    )
except Exception as e:
    st.error(f"Weather data read failed: {e}")
    weather_df = pd.DataFrame()

st.subheader("Weather Data (Last 50 entries)")

if not weather_df.empty:
    st.dataframe(weather_df)

    # Weather chart
    if "temperature" in weather_df.columns:
        st.line_chart(
            weather_df[["timestamp", "temperature"]].set_index("timestamp")
        )
else:
    st.write("Ei säätietoja saatavilla.")

# -------------------------
# AVIATION DATA
# -------------------------
try:
    aviation_df = pd.read_sql(
        "SELECT * FROM aviation_data ORDER BY id DESC LIMIT 200",
        conn
    )
except Exception as e:
    st.error(f"Aviation data read failed: {e}")
    aviation_df = pd.DataFrame()

st.subheader("Aviation Data (Latest entries)")

if not aviation_df.empty:
    st.dataframe(aviation_df)

    # Funktio puhdistaa departure-sarakkeen datetimeksi
    def extract_departure_time(dep):
        if dep is None:
            return None
        if isinstance(dep, pd.Timestamp):
            return dep
        dep_str = str(dep)
        match = re.search(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}", dep_str)
        if match:
            return pd.to_datetime(match.group(0))
        return None

    aviation_df["dep_clean"] = aviation_df["departure"].apply(extract_departure_time)
    aviation_df = aviation_df.dropna(subset=["dep_clean"])

    if not aviation_df.empty:
        st.subheader("Aviation Chart – Flights Over Time")
        st.line_chart(
            aviation_df[["dep_clean", "id"]].set_index("dep_clean")
        )
    else:
        st.write("Ei kelvollisia lähtöaikoja kaavion piirtämiseen.")
else:
    st.write("Ei ilmailutietoja saatavilla.")

# -------------------------
# Close DB connection
# -------------------------
conn.close()
