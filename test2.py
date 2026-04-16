import pandas as pd

def get_calc_constants(liquid_name):
    df = pd.read_csv('data_file.csv')
    df.columns = df.columns.str.strip()
    
    match = df[df['name'].str.contains(liquid_name, case=False, na=False)]
    
    if not match.empty:
        row = match.iloc[0]
        return {
            "name": row['name'],
            "Tc": row['critical temperature (K)'],
            "omega": row['acentric factor'],
            "actual_bp": row['boiling point (K)'] # Adding this for testing!
        }
    return None

# --- THE CALCULATOR ---
user_query = input("Enter liquid to calculate: ")
data = get_calc_constants(user_query)

if data:
    # 1. Get the constants
    Tc = data['Tc']
    w = data['omega']
    actual = data['actual_bp']
    
    # 2. THE CALCULATION
     
    calculated_bp = Tc * (0.567 + (0.106 * w))
    
    # 3. PRINT RESULTS & TEST
    print(f"\n--- Results for {data['name']} ---")
    print(f"Calculated BP: {calculated_bp:.2f} K")
    print(f"Actual BP (from file): {actual} K")
    
    print("Test- Calculate error percentage to see how right we are")
    error = abs(calculated_bp - actual) / actual * 100
    print(f"Calculation Error: {error:.2f}%")
    
else:
    print("Liquid not found.")