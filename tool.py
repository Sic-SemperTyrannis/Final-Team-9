# tool.py
# -------------------------------------------------------
# Tool Name : Calculate Diffrent Fluid Properties
# Domain : Engineering
# Description: Takes a few fluid properties and extrapolate other properties
# and why it matters in the domain> Matters for thermodynamics calculations

# -------------------------------------------------------
def fluid_properties(density, specific_heat, initial_temp, final_temp,
                     volume, boiling_temp, latent_heat) -> dict:
    """
    Computes thermodynamic properties including phase change and boiling energy.
    """

    # --- Input Validation ---
    if density <= 0:
        return {"result": None, "unit": "J", "detail": "Density must be > 0."}

    if specific_heat <= 0:
        return {"result": None, "unit": "J", "detail": "Specific heat must be > 0."}

    if volume <= 0:
        return {"result": None, "unit": "J", "detail": "Volume must be > 0."}

    if latent_heat < 0:
        return {"result": None, "unit": "J", "detail": "Latent heat cannot be negative."}

    if initial_temp == final_temp:
        return {
            "result": 0,
            "unit": "J",
            "detail": "No temperature change → no heat transfer."
        }

    if boiling_temp < -273.15:
        return {
            "result": None,
            "unit": "J",
            "detail": "Boiling temperature is below absolute zero."
        }

    # --- Core Logic ---
    mass = density * volume
    delta_T = final
