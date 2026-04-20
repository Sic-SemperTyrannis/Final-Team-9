import csv
import os

def get_calc_constants(liquid_name):
    """
    Retrieves constants from data_file.csv and maps them to names
    the app.py and tool.py expect.
    """
    # Get the correct path to the CSV file
    base_path = os.path.dirname(__file__)
    csv_path = os.path.join(base_path, 'data_file.csv')

    try:
        with open(csv_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Search for the liquid name (case-insensitive)
                if row['name'].strip().lower() == liquid_name.strip().lower():
                    return {
                        "name": row['name'],
                        # Map 'critical temperature (K)' from CSV to 'Tc' for app.py
                        "Tc": float(row['critical temperature (K)']),
                        # Map 'boiling point (K)' and convert to Celsius for tool.py
                        "boiling_temp": float(row['boiling point (K)']) - 273.15,
                        "omega": float(row['acentric factor']),
                        "molweight": float(row['molweight']),
                        # Placeholders for values not in your current CSV
                        "density": 1000, 
                        "specific_heat": 4184,
                        "latent_heat": 2260000 
                    }
    except FileNotFoundError:
        print("Error: data_file.csv not found.")
    except KeyError as e:
        print(f"Error: Missing column in CSV: {e}")
    
    return None
# (+)-a-pinene