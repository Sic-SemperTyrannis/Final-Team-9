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
with st.form("input_form"):
    liquid_name = st.text_input("Enter liquid name:")
    liquid_final_temp = st.text_input("Enter temperature to heat liquid:")
    liquid_initial_temp = st.text_input("Enter intial temperature:")
    liquid_volume = st.text_input("Enter liquid volume:")
    use_ai = st.checkbox("Explain result with Gemini AI")
    submitted = st.form_submit_button("Calculate")

if submitted:
    if not liquid_name.strip():
        st.warning("Please enter a liquid name.")
    else:
        data = get_calc_constants(liquid_name)

        if data:
            # RAG 1
            result = fluid_properties(
                density=data["density"],
                specific_heat=data["specific_heat"],
                initial_temp=liquid_initial_temp, 
                final_temp=liquid_final_temp,
                volume=liquid_volume,
                boiling_temp=data["boiling_temp_c"],
                latent_heat=data["latent_heat"]
            )

            #Output. Gives user the reults of the boiling calculations
            st.subheader(f"Results for {data['name']}")

            if result["result"] is None:
                st.error(result["detail"])
            else:
                st.metric("Energy Required (J)", f"{result['result']:.2f}")
                st.metric("Mass (kg)", f"{result['properties']['mass (kg)']:.2f}")
                st.metric("Boiling Point (°C)", f"{data['boiling_temp_c']:.2f}")

                if use_ai: #(This prompts the Ai and gets the output formatted as desgnated)
                    prompt = f" Explain the calculations result briefly: Fluid: {data['name']} Energy Required: {result['result']} J Boiling Point: {data['boiling_temp_c']} °C Keep it under 3 sentences and simple."
                    explanation = ask_llm(prompt)
                    st.write(explanation)

            # Option to generate heating design
            st.subheader("Heating System Design")
            if st.button("Generate Heating Design"):
                design_prompt = f"Provide a heating system design for {data['name']} to reach {liquid_final_temp}°C from {liquid_initial_temp}°C for {liquid_volume} m³. Include type of machinery, materials, and steps in plain English."
                design_instructions = ask_llm(design_prompt)
                st.write(design_instructions)
