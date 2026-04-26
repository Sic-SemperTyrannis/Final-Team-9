#Needs to be able to take and output data in streamlit make it looka pretty and clean
import streamlit as st
from test2 import get_calc_constants
from tool import fluid_properties # This is for RAG1 comment out later if teamates develop something better. 
#We were still discussing which file to run RAG through I just threw a preliminary one in here
from agent import ask_llm

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
        # Retrieve constants from CSV database
        data = get_calc_constants(liquid_name)
        if not data:
            st.error(f"Liquid '{liquid_name}' not found in database.")
        else:
            # Calculate fluid properties safely
            result = fluid_properties(
                density=data.get("density", 0),
                specific_heat=data.get("specific_heat", 0),
                initial_temp=float(liquid_initial_temp),
                final_temp=float(liquid_final_temp),
                volume=float(liquid_volume),
                boiling_temp=data.get("boiling_temp_c", 100),
                latent_heat=data.get("latent_heat", 0)
            )

            if result is None:
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
        st.metric("Energy Required (J)", f"{result['result']:.2f}")
        st.metric("Mass (kg)", f"{result['properties']['mass (kg)']:.2f}")
        st.metric("Boiling Point (°C)", f"{data['boiling_temp_c']:.2f}")

        if use_ai:
            prompt = f" Explain the calculations result briefly: Fluid: {data['name']} Energy Required: {result['result']} J Boiling Point: {data['boiling_temp_c']} °C Keep it under 3 sentences and simple."
            explanation = ask_llm(prompt)
            st.write(explanation)

    # Option to generate heating design
    st.subheader("Heating System Design")
    if st.button("Generate Heating Design"):
        design_prompt = f"Provide a heating system design for {data['name']} to reach {liquid_final_temp}°C from {liquid_initial_temp}°C for {liquid_volume} m³. Include type of machinery, materials, and steps in plain English."
        design_instructions = ask_llm(design_prompt)
        st.write(design_instructions)