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
    delta_T = final_temp - initial_temp
    latent_energy =0
    

    if initial_temp < boiling_temp:
        Q_to_boil = mass * specific_heat * (boiling_temp - initial_temp)

    if final_temp < boiling_temp:
        Q = mass * specific_heat * delta_T
    else:
        if initial_temp < boiling_temp:
            phase_change = True 
            latent_energy = mass * latent_heat
            Q = Q_to_boil + latent_energy
        else:
            Q = mass * specific_heat * delta_T
    
    energy_per_volume = Q / volume

    return {
        "result": Q,
        "unit": "J",
        "detail": f"m={mass} kg, ΔT={delta_T}°C",
        "properties": {
            "mass (kg)": mass,
            "temperature_change (°C)": delta_T,
            "boiling_point (°C)": boiling_temp,
            "energy_to_reach_boiling (J)": Q_to_boil,
            "latent_heat_added (J)": latent_energy,
            "energy_per_volume (J/m^3)": energy_per_volume
        }
    }
