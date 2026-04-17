#Needs to be able to take and output data in streamlit make it looka pretty and clean
import streamlit as st
from test2 import get_calc_constants
from agent import ask_llm

st.set_page_config(page_title="Boiling Point Calculator", layout="centered")

st.title("Liquid Boiling Point Calculator")

st.write(
    "Enter a liquid name to calculate its boiling point."
)

liquid_name = st.text_input("Enter liquid name:")

use_ai = st.checkbox("Explain result with Gemini AI")

if st.button("Calculate"):
    if not liquid_name.strip():
        st.warning("Please enter a liquid name.")
    else:
        data = get_calc_constants(liquid_name)

        if data:
            Tc = data['Tc']
            w = data['omega']
            actual = data['actual_bp']

            # Calculate
            calculated_bp = Tc * (0.567 + (0.106 * w))
            error = abs(calculated_bp - actual) / actual * 100

            #Resalts
            st.subheader(f"Results for {data['name']}")
            st.metric("Calculated Boiling Point (K)", f"{calculated_bp:.2f}")
            st.metric("Actual Boiling Point (K)", f"{actual}")
            st.metric("Error (%)", f"{error:.2f}")

    else:
  st.error("Liquid entry error. Liquid is not in database")
