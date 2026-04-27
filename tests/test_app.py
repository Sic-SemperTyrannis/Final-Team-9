bboyblake
bboyblake
In a call

Will — 4/22/2026 7:52 PM
If you need anything let me knwo
bboyblake — 4/22/2026 7:52 PM
{
    "density": 1000,
    "specific_heat": 4200,
    "boiling_temp": 100,
    "latent_heat": 334000
}

this is output from the llm how accurate does this look to you?
Will — 4/22/2026 7:53 PM
for water that is perfect
bboyblake — 4/22/2026 7:55 PM
yea the problem is its pretty much just a string and i have to figure out a way to extract only the numbers and make sure it is a decimal variable type because he said he wants no floating point numbers in the calculations I'm also running out of tokens 🙁 
Will — 4/22/2026 7:55 PM
Mabye you can try just testing in a diffrent llm
bboyblake — 4/22/2026 7:59 PM
I could but feel like that would only help if I run out of tokens to test with because the data is very accurate only off by about 5% is the most i have seen so far but the problem i have is extracting the data from the outputted string
i can probably figure it out tonight if anyone wants to work on rag 2 it will probably be much easier because you don't need to return hard values
Will — 4/22/2026 8:00 PM
sounds good
bboyblake — 4/22/2026 8:03 PM
at this point we could also argue that the another use of the agent is fast accurate RAG data retrieval of any given fluid
DaniJay — 4/22/2026 9:05 PM
Im checked out for tonight but I can help/start with rag2 tomorrow
DaniJay — 4/24/2026 4:06 PM
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools import DuckDuckGoSearchRun
from dotenv import load_dotenv
from tool import fluid_properties
import os

agent.py
4 KB
bboyblake — 4/24/2026 4:07 PM
I got rag 1 to work! im gonna make a few adjustments before the first push though
it works with my test of hardcoding what would be the user input, you can also see the raw output of the llm and so far its made no mistakes. @Will when you get the chance can you look over this output real quick?

Will — 4/24/2026 4:23 PM
Thats perfect great job, just have to geat it to output out of streamlit
bboyblake — 4/24/2026 4:27 PM
i did notice though that me and Dani's have some variable conflicts that we need to sort out and we both implemented rag 1 so we will have to discus which rag one will work better form what I have seen so far her rag 2 looks great and her llm_calculation_interpretation promt looks 10X better than the placeholder one I have now once we merge and figure out the variable conflicts all we have to do is apply it in stream-lit and debug
I told chat gpt our layout plan and I think It came up with something great for us to base it off of and easy to follow and implement
Image
bboyblake
 started a call that lasted 42 minutes. — 4/24/2026 7:01 PM
DaniJay — 4/24/2026 7:11 PM
Hey sorry im not going to be able to join I have to head home unexpectedly
Can yall give key pointers whenever
Wait I just cant talk
Yes im in a car not driving tho so I can pay attention
Yeah we can definitely use your rag 1 i wasnt sure on it anyway that why I sent it to you first lol
Im glad the rest looks good 👍
Waiiiiiit
I camt push so I sent it here idk whats up with my repository
No
Correct
DaniJay — 4/24/2026 7:18 PM
Yes I see thank you
I got to hang up bye guys
bboyblake — Yesterday at 2:02 PM
all rag systems functional
Will — 1:32 PM
Whats left to get the code working
Grady — 2:00 PM
im working on modifying the streamlit. Its being fussy
Will — 2:00 PM
Cool im finishing up the paper now
bboyblake
 started a call that lasted 4 hours. — 2:17 PM
bboyblake — 2:28 PM
run_calculation, llm_calculation_interpretation, rag_heating_consultant
bboyblake — 2:49 PM
data, result = run_calculation(
        liquid_name,
        float(liquid_initial_temp),
        float(liquid_final_temp),
        float(liquid_volume)
    )
Grady — 3:29 PM
File "/workspaces/Final-Team-9/.venv/lib/python3.12/site-packages/streamlit/runtime/scriptrunner/exec_code.py", line 129, in exec_func_with_error_handling
    result = func()
             ^^^^^^
File "/workspaces/Final-Team-9/.venv/lib/python3.12/site-packages/streamlit/runtime/scriptrunner/script_runner.py", line 689, in code_to_exec
    exec(code, module.dict)  # noqa: S102
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/workspaces/Final-Team-9/app.py", line 34, in <module>
    data, result = run_calculation(
                   ^^^^^^^^^^^^^^^
Grady — 3:37 PM
KeyError: 'boiling_temp_c'
Traceback:
File "/workspaces/Final-Team-9/.venv/lib/python3.12/site-packages/streamlit/runtime/scriptrunner/exec_code.py", line 129, in exec_func_with_error_handling
    result = func()
             ^^^^^^
File "/workspaces/Final-Team-9/.venv/lib/python3.12/site-packages/streamlit/runtime/scriptrunner/script_runner.py", line 689, in code_to_exec
    exec(code, module.dict)  # noqa: S102
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/workspaces/Final-Team-9/app.py", line 57, in <module>
    st.metric("Boiling Point (°C)", f"{float(data['boiling_temp_c']):.2f}")
                                             ~~~~^^^^^^^^^^^^^^^^^^
KeyError: 'boiling_point'
Traceback:
File "/workspaces/Final-Team-9/.venv/lib/python3.12/site-packages/streamlit/runtime/scriptrunner/exec_code.py", line 129, in exec_func_with_error_handling
    result = func()
             ^^^^^^
File "/workspaces/Final-Team-9/.venv/lib/python3.12/site-packages/streamlit/runtime/scriptrunner/script_runner.py", line 689, in code_to_exec
    exec(code, module.dict)  # noqa: S102
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/workspaces/Final-Team-9/app.py", line 57, in <module>
    st.metric("Boiling Point (°C)", f"{float(data['boiling_point']):.2f}")
                                             ~~~~^^^^^^^^^^^^^^^^^
bboyblake — 3:41 PM
boiling_point (°C)
st.metric("Boiling Point (°C)", f"{float(result['properties']['boiling_point (°C)']):.2f}")
Grady — 3:54 PM
Image
bboyblake — 3:55 PM
#1 rag 2 promt
#2 metrics
#3 if not liquid rag #3
temp change,
energy to boiling
Latent  heat added
Grady — 4:32 PM
Image
bboyblake — 5:42 PM
@everyone app is practically finished, still need to deploy it and add secrets
Will — 5:44 PM
If yall want to jump on a call at like 7 we can finish it
bboyblake
 started a call. — 7:02 PM
bboyblake — 7:13 PM
#1 dir structure
#2 secrets
#3 test.py
#4 upload
#5 word doc/ make sure to show populated project board
#6 video
DaniJay — 7:31 PM
im working on that rn
if it doesn't show up submitted for all of us when one person turns it in, then we all have to. it just something we have to check thats all 
Grady — 7:52 PM
Good shout, we should definitely be wary of that
Will — 8:00 PM
Image
import pytest
import concurrent.futures
from unittest.mock import patch

# Import your actual functions
from test2 import get_calc_constants

message.txt
5 KB
Will — 8:34 PM
AIzaSyAF1R69mNx0tLQb8wsDm6gMqpvGi2bsYDk
DaniJay — 8:36 PM
nope
oh wait he is so right
Will — 8:51 PM
LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT=https://api.smith.langchain.com/
LANGSMITH_API_KEY=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
LANGSMITH_PROJECT="Final Project"
﻿
import pytest
import concurrent.futures
from unittest.mock import patch

# Import your actual functions
from test2 import get_calc_constants
from tool import fluid_properties
from agent import ask_llm


# =========================================================
# 🔷 UNIT TESTS
# =========================================================

# -------- RAG 1: Data Retrieval --------
def test_get_calc_constants_valid():
    data = get_calc_constants("water")
    assert data is not None
    assert "density" in data
    assert "specific_heat" in data
    assert data["boiling_temp_c"] > 0


def test_get_calc_constants_invalid():
    data = get_calc_constants("invalid_fluid")
    assert data is None


# -------- Calculation Engine --------
def test_fluid_properties_basic():
    result = fluid_properties(
        density=1000,
        specific_heat=4186,
        initial_temp=25,
        final_temp=100,
        volume=1,
        boiling_temp=100,
        latent_heat=2260000
    )

    assert result["result"] is not None
    assert result["properties"]["mass (kg)"] == 1000


def test_fluid_properties_invalid():
    result = fluid_properties(
        density=-1,
        specific_heat=4186,
        initial_temp=25,
        final_temp=100,
        volume=1,
        boiling_temp=100,
        latent_heat=2260000
    )

    assert result["result"] is None


# -------- RAG 2: LLM (Mocked) --------
@patch("agent.ask_llm")
def test_llm_mock(mock_llm):
    mock_llm.return_value = "Use an electric heater with stainless steel."

    response = ask_llm("test prompt")
    assert isinstance(response, str)
    assert "heater" in response.lower()


# =========================================================
# 🔷 INTEGRATION TESTS
# =========================================================

def test_full_pipeline():
    data = get_calc_constants("water")
    assert data is not None

    result = fluid_properties(
        density=data["density"],
        specific_heat=data["specific_heat"],
        initial_temp=25,
        final_temp=100,
        volume=1,
        boiling_temp=data["boiling_temp_c"],
        latent_heat=data["latent_heat"]
    )

    assert result["result"] > 0


def test_parallel_rag():
    def rag1():
        return get_calc_constants("water")

    def rag2():
        return "Mock heating system"

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future1 = executor.submit(rag1)
        future2 = executor.submit(rag2)

        data = future1.result()
        design = future2.result()

    assert data is not None
    assert isinstance(design, str)


# =========================================================
# 🔷 LOAD / STRESS TEST
# =========================================================

def simulate_request():
    data = get_calc_constants("water")
    if not data:
        return False

    result = fluid_properties(
        density=data["density"],
        specific_heat=data["specific_heat"],
        initial_temp=25,
        final_temp=100,
        volume=1,
        boiling_temp=data["boiling_temp_c"],
        latent_heat=data["latent_heat"]
    )

    return result["result"] is not None


def test_load():
    NUM_REQUESTS = 50  # benchmark target

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(lambda _: simulate_request(), range(NUM_REQUESTS)))

    assert all(results)


# =========================================================
# 🔷 OPTIONAL: PERFORMANCE CHECK
# =========================================================

def test_response_time():
    import time

    start = time.time()

    data = get_calc_constants("water")
    result = fluid_properties(
        density=data["density"],
        specific_heat=data["specific_heat"],
        initial_temp=25,
        final_temp=100,
        volume=1,
        boiling_temp=data["boiling_temp_c"],
        latent_heat=data["latent_heat"]
    )

    end = time.time()

    assert result["result"] is not None
    assert (end - start) < 3  # should respond within 3 seconds