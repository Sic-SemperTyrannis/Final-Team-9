#llm calculator prompts and testing
"""
How to test yourself on your own branch

(intall dependancies)
pip install langchain-google-genai
pip install python-dotenv

(.env)
in the .env file put in your google api key


run agent.py
"""
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from tool import fluid_properties
import os

#loads api key
load_dotenv()

#initializes gemini
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)

#LLm call 
def ask_llm(prompt):
    response = llm.invoke(prompt)
    return response.content

def llm_calculation_interpretation(data, result):
    #invalid calulation case
    if result["result"] is None:
        return f"Calculation could not be performed: {result['detail']}"

    #if there was no temperature change
    if result["result"] == 0:
        return "No energy transfer occurs because there is no temperature change."
    
    #prompts the llm to breifly explain the calulations and if there are any potential engineering applications
    prompt = f"""
    Explain these thermodynamics calculations in exactly 3 short sentences:
    
    context: This calculation estimates the energy needed to heat up a fluid and acount for phase change if the fluid boils

    Fluid: {data['name']}

    Energy required: {result['result']} J
    Mass: {result['properties']['mass (kg)']} kg
    Temperature change: {result['properties']['temperature_change (°C)']} °C
    Boiling point: {result['properties']['boiling_point (°C)']} °C
    Energy to reach boiling: {result['properties']['energy_to_reach_boiling (J)']} J
    Latent heat added: {result['properties']['latent_heat_added (J)']} J
    
    Sentence 1: Briefly explain what the calculation represents
    Sentence 2: Mention one key assumption
    Sentence 3: mention one realistic engineering application

    keep the explanation easy to understand
    -DO NOT overexplain intermediate values
    -Do NOT use bullet points
    """
    return ask_llm(prompt)


#tesing the LLM function (Placeholder values) Calls the agent calculator prompt and also prints the raw data recieved from tool.py
if __name__ == "__main__":
    
    data = {"name": "water"}

    result = fluid_properties(
        density=1000,
        specific_heat=4184,
        initial_temp=20,
        final_temp=100,
        volume=1,
        boiling_temp=100,
        latent_heat=2260000
    )

    print("RAW RESULT:")
    print(result)

    print("Agent interpitation:")
    print(llm_calculation_interpretation(data, result))