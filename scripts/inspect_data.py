import pandas as pd

# Load dataset
df = pd.read_json(r"C:\Users\sri tejasw\biztelai\data\BiztelAI_DS_Dataset_Mar'25.json")

# Transpose the dataframe so transcript IDs are rows, not columns
df = df.T  

# Print dataset structure
print(df.head())

# Save the fixed dataset (optional)
df.to_json(r"C:\Users\sri tejasw\biztelai\data\BiztelAI_DS_Fixed.json", orient="records")
