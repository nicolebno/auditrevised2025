import pandas as pd
import hashlib

def debug_print(message, df=None):
    print(f"[DEBUG] {message}")
    if df is not None:
        print(df.head())
        print(f"Columns: {list(df.columns)}\n")

def validate_input_file(df, required_columns, file_name):
    df.columns = df.columns.str.strip().str.upper()
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise KeyError(f"{file_name} is missing required columns: {missing_columns}")

def compare_files(df_census, df_carrier):
    # Normalize names
    df_census['FIRST NAME'] = df_census['FIRST NAME'].str.strip().str.replace(r"[\s-]", "", regex=True).str.lower()
    df_census['LAST NAME'] = df_census['LAST NAME'].str.strip().str.replace(r"[\s-]", "", regex=True).str.lower()
    df_carrier['FIRST NAME'] = df_carrier['FIRST NAME'].str.strip().str.replace(r"[\s-]", "", regex=True).str.lower()
    df_carrier['LAST NAME'] = df_carrier['LAST NAME'].str.strip().str.replace(r"[\s-]", "", regex=True).str.lower()

    combined = pd.merge(
        df_census,
        df_carrier,
        on=["FIRST NAME", "LAST NAME"],
        how="outer",
        suffixes=('_census', '_carrier'),
        indicator=True
    )

    combined = combined[~(combined['FIRST NAME'].isna() & combined['LAST NAME'].isna())]
    combined['STATUS'] = 'Valid'
    combined['ISSUE'] = None

    for idx, row in combined.iterrows():
        if row['_merge'] == 'left_only':
            combined.at[idx, 'STATUS'] = 'Invalid'
            combined.at[idx, 'ISSUE'] = 'Missing Carrier Premium'
        elif row['_merge'] == 'right_only':
            combined.at[idx, 'STATUS'] = 'Invalid'
            combined.at[idx, 'ISSUE'] = 'Missing Census Premium'
        elif pd.isna(row['TOTAL PREMIUM']) or pd.isna(row['CARRIER PREMIUM']):
            combined.at[idx, 'STATUS'] = 'Invalid'
            combined.at[idx, 'ISSUE'] = 'Missing Premium Data'
        elif row['TOTAL PREMIUM'] != row['CARRIER PREMIUM']:
            combined.at[idx, 'STATUS'] = 'Invalid'
            combined.at[idx, 'ISSUE'] = 'Premium Mismatch'

    combined.drop(columns=['_merge'], inplace=True)
    combined['UNIQUE ID'] = combined.apply(
        lambda x: hashlib.sha256(f"{x['FIRST NAME']}{x['LAST NAME']}".encode()).hexdigest()[:8]
        if pd.notna(x['FIRST NAME']) and pd.notna(x['LAST NAME']) else None,
        axis=1
    )
    combined = combined[~combined['UNIQUE ID'].isna()]
    combined = combined[['UNIQUE ID', 'FIRST NAME', 'LAST NAME', 'TOTAL PREMIUM', 'CARRIER PREMIUM', 'STATUS', 'ISSUE']]
    return combined

def create_templates():
    census_template = pd.DataFrame({
        'FIRST NAME': [],
        'LAST NAME': [],
        'TOTAL PREMIUM': []
    })
    carrier_template = pd.DataFrame({
        'FIRST NAME': [],
        'LAST NAME': [],
        'CARRIER PREMIUM': []
    })

    census_template.to_excel("Census_Template.xlsx", index=False)
    carrier_template.to_excel("Carrier_Template.xlsx", index=False)
