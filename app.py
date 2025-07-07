import streamlit as st
import pandas as pd
import joblib

# Load model and columns
model = joblib.load("pollution_model.pkl")
model_columns = joblib.load("model_columns.pkl")

st.title("🌊 Water Quality Forecasting (Southern Bug River)")

station_id = st.text_input("Enter Station ID (e.g. 22)", "22")
year_input = st.number_input("Enter Year", min_value=2000, max_value=2100, value=2024)

if st.button("Predict Pollutants"):
    input_df = pd.DataFrame({'year': [year_input], 'id': [station_id]})
    input_encoded = pd.get_dummies(input_df, columns=['id'])

    missing_cols = set(model_columns) - set(input_encoded.columns)
    for col in missing_cols:
        input_encoded[col] = 0
    input_encoded = input_encoded[model_columns]

    prediction = model.predict(input_encoded)[0]
    pollutants = ['O2', 'NO3', 'NO2', 'SO4', 'PO4', 'CL']

    st.subheader(f"Predicted Pollutants for Station {station_id} in {year_input}:")
    for p, val in zip(pollutants, prediction):
        st.write(f"{p}: {val:.2f}")
