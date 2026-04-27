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