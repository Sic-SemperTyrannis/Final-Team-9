import os
import csv

def get_calc_constants(fluid_id):
    """
    Searches data_file.csv by ID and returns the physical properties.
    Using 'utf-8-sig' to handle potential Excel/Windows hidden characters.
    """
    # Locates the CSV in the same folder as this script
    base_path = os.path.dirname(__file__)
    csv_path = os.path.join(base_path, 'data_file.csv')
    
    try:
        if not os.path.exists(csv_path):
            print(f"Error: Could not find {csv_path}")
            return None

        with open(csv_path, mode='r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Strip spaces from keys and values to prevent KeyErrors
                clean_row = {k.strip(): v.strip() for k, v in row.items() if k}
                
                if clean_row.get('id') == str(fluid_id):
                    return {
                        "name": clean_row.get('name'),
                        "density": float(clean_row.get('density', 0)),
                        "specific_heat": float(clean_row.get('specific_heat', 0)),
                        "boiling_temp_c": float(clean_row.get('boiling_point_k', 273.15)) - 273.15,
                        "latent_heat": float(clean_row.get('latent_heat', 0))
                    }
    except Exception as e:
        print(f"Data Retrieval Error: {e}")
    
    return None
