import streamlit as st
import mysql.connector
import pandas as pd

st.set_page_config(page_title="Weather & Aviation Data", layout="wide")
st.title("Weather & Aviation Data Dashboard")

try:
    # Yhdistä MySQL-tietokantaan
    conn = mysql.connector.connect(
        host='localhost',
        user='VITTU',
        password='Moimoi33-',
        database='weather'
    )

    # --- Weather Data ---
    weather_df = pd.read_sql(
        'SELECT * FROM weather_data ORDER BY timestamp DESC LIMIT 50', conn
    )

    st.subheader("Weather Data (Last 50 entries)")
    if not weather_df.empty:
        st.dataframe(weather_df)
    else:
        st.write("Ei säätietoja saatavilla.")

    # --- Aviation Data ---
    aviation_df = pd.read_sql(
        'SELECT * FROM aviation_data ORDER BY timestamp DESC LIMIT 50', conn
    )

    st.subheader("Aviation Data (Last 50 entries)")
    if not aviation_df.empty:
        st.dataframe(aviation_df)
    else:
        st.write("Ei ilmailutietoja saatavilla.")

    conn.close()

except mysql.connector.Error as e:
    st.error(f"Tietokantavirhe: {e}")

