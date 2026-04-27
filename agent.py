#llm calculator prompts and testing
"""
How to test yourself on your own branch
(intall dependancies)
pip install langchain-google-genai python-dotenv langchain-community duckduckgo-search ddgs streamlit
(.env)
in the .env file put in your google api key
run agent.py
"""
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from tool import fluid_properties
import os
import ast
from decimal import Decimal
from langchain_community.tools import DuckDuckGoSearchRun
import re
from langsmith import traceable
from tool import fluid_properties
search = DuckDuckGoSearchRun()

#loads api key
load_dotenv()

#initializes gemini
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    temperature=0
)

#LLm call 
@traceable(name="LLM Call")
def ask_llm(prompt):
    response = llm.invoke(prompt)
    return response.content
#-------------RAG1_Search_Query-----------------
def rag_variable_retriever(fluid_name):

    query = f"{fluid_name} properties density kg/m3 specific heat J/kgK boiling point C latent heat J/kg engineering toolbox"

    raw_search_results = search.run(query)

    extraction_prompt = f"""
    Extract numerical thermodynamic properties for {fluid_name}.

    Return ONLY a Python dictionary:

    {{
        "density": value,
        "specific_heat": value,
        "boiling_temp": value,
        "latent_heat": value
    }}

    Rules:
    - density in kg/m^3
    - specific_heat in J/kg°C
    - boiling_temp in °C
    - latent_heat in J/kg
    - Values MUST be numbers (no text, no units)
    - If unsure, estimate a reasonable engineering value
    - DO NOT return null
    - DO NOT explain anything

    Text:
    {raw_search_results}
    """

    response = llm.invoke(extraction_prompt)

    return response.content


#-----------Parsing_Of_LLM_String-----------------
@traceable(name="RAG 1 - Variable Retrieval")
def rag_lookup(fluid_name, retries=1):

    for _ in range(retries):

        raw = rag_variable_retriever(fluid_name)
        print("\nRAW LLM OUTPUT:")
        print(raw)
        try:
            raw = raw.strip()
            # remove markdown code blocks if present
            raw = re.sub(r"```[\w]*\n?", "", raw).strip()
            raw = raw.rstrip("`").strip()
            parsed = None
            parsed = ast.literal_eval(raw)

        except Exception as e:
            print(f"Parse attempt failed: {e}")
            continue

        if not parsed:
            continue

        try:
            data = {
                "name": fluid_name,
                "density": Decimal(str(parsed.get("density"))),
                "specific_heat": Decimal(str(parsed.get("specific_heat"))),
                "boiling_temp": Decimal(str(parsed.get("boiling_temp"))),
                "latent_heat": Decimal(str(parsed.get("latent_heat")))
            }

            return data

        except:
            continue

    return None


@traceable(name="RAG 2 - Heating Design")
def rag_heating_consultant(data, result):
    if result["result"] is None:
        return f"Calculation could not be performed: {result['detail']}"
    
    prompt = f"""
    Analyze the following heating system requirements for {data['name']}:
    Energy Needed: {result['result']} J | Mass: {result['properties']['mass (kg)']} kg
    
    REQUIRED OUTPUT:
    1. RECOMMENDED MACHINERY
    2. MATERIAL COMPATIBILITY
    3. SAFETY CONSTRAINTS
    4. SETUP STEPS

    Keep each section to 2-3 bullet points maximum. Be concise and technical.
    """

    return ask_llm(prompt)


#-----------LLM_CALCULATOR_PROMT-----------------
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
    print(f"""
    Fluid Properties Retrieved:
    - Fluid: {data['name']}
    - Density: {data['density']} kg/m³
    - Specific Heat: {data['specific_heat']} J/kg°C
    - Boiling Point: {data['boiling_temp']} °C
    - Latent Heat: {data['latent_heat']} J/kg
    """)


    return ask_llm(prompt)


#determine if user input is a valid fluid
def is_valid_fluid(fluid_name):
    prompt = f"""
    Is "{fluid_name}" a fluid or liquid that has thermodynamic properties like density, specific heat, and boiling point?
    Answer only "yes" or "no".
    """
    response = ask_llm(prompt)
    return response.strip().lower() == "yes"




#used to transfer RAG_1 data into tool.py

@traceable(name="Full Calculation Pipeline")
def run_calculation(fluid_name, initial_temp, final_temp, volume):
    data = rag_lookup(fluid_name)

    if data is None:
        return None, {"result": None, "detail": f"Could not retrieve properties for {fluid_name}"}

    result = fluid_properties(
        density=data["density"],
        specific_heat=data["specific_heat"],
        initial_temp=Decimal(str(initial_temp)),
        final_temp=Decimal(str(final_temp)),
        volume=Decimal(str(volume)),
        boiling_temp=data["boiling_temp"],
        latent_heat=data["latent_heat"]
    )

    return data, result

#tesing prints the raw data recieved from tool.py, shows LLM raw output returns the data it finds and test plugging the decimal values into the calulator
if __name__ == "__main__":
    data, result = run_calculation("water", 20, 120, 1)
    print("\nCALCULATION RESULT:")
    print(result)
    print("\nINTERPRETATION:")
    print(llm_calculation_interpretation(data, result))
    print("\nHEATING SYSTEM DESIGN:")
    print(rag_heating_consultant(data, result))



