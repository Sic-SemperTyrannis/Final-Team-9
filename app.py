#Needs to be able to take and output data in streamlit make it looka pretty and clean
import streamlit as st
from test2 import get_calc_constants
from agent import ask_llm, run_calculation, llm_calculation_interpretation, rag_heating_consultant

st.set_page_config(page_title="Boiling Point Calculator", layout="centered")
st.title("Liquid Boiling Point Calculator")
st.write("Enter a liquid name to calculate its boiling point.")

#Add support for both RAG's rag 1 - retrivial tool calculation variables  takes the name and finds all necessity variable's for calculation
#rag 2 - takes data about the given fluid and possible constraints due to its nature 
#to then output to the user what kind heating system would need to be set up, such as type of machinery and materials and give steps on how to set it up2

if "calculated" not in st.session_state:
    st.session_state.calculated = False
    st.session_state.result = None
    st.session_state.data = None

with st.form("input_form"):
    liquid_name = st.text_input("Enter liquid name:")
    liquid_initial_temp = st.number_input("Enter initial temperature (°C):", value=25.0)
    liquid_final_temp = st.number_input("Enter temperature to heat liquid (°C):", value=100.0)
    liquid_volume = st.number_input("Enter liquid volume (m³):", value=1.0, min_value=0.0)
    use_ai = st.checkbox("Explain result with Gemini AI")
    submitted = st.form_submit_button("Calculate")

if submitted:
    if not liquid_name.strip():
        st.warning("Please enter a liquid name.")
    else:
        with st.spinner(text="Gathering fluid properties..."):
            data, result = run_calculation(
                liquid_name,
                float(liquid_initial_temp),
                float(liquid_final_temp),
                float(liquid_volume)
            )

        if data is None:
                st.error("Calculation failed due to invalid inputs.")
        else:
                st.session_state.calculated = True
                st.session_state.result = result
                st.session_state.data = data

# Display results if calculation succeeded
if st.session_state.calculated:
    data = st.session_state.data
    result = st.session_state.result

    st.subheader(f"Results for {data['name']}")
    if result is None or result.get("result") is None:
        st.error(result["detail"] if result else "Calculation could not be performed.")
    else:
        st.metric("Energy Required (J)", f"{float(result['result']):.2f}")
        st.metric("Mass (kg)", f"{float(result['properties']['mass (kg)']):.2f}")
        st.metric("Boiling Point (°C)", f"{float(result['properties']['boiling_point (°C)']):.2f}")

        if use_ai:
            st.subheader("Calculation interpretation")
            with st.spinner(text="Generating calculation interpretation..."):
                explanation = llm_calculation_interpretation(data, result)
            st.write(explanation)

    # Option to generate heating design
    st.subheader("Heating System Design")
    if st.button("Generate Heating Design"):
        with st.spinner(text="Generating Heating Design..."):
           design_instructions = rag_heating_consultant(data, result)
        st.write(design_instructions)