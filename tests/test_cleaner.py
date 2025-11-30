
import pandas as pd
def currency_val(currency):
  return currency in ["IDR", "USD", "SGD"]
def validate_date_format(date_string):
    """
    Validate if date string is in YYYY-MM-DD or DD/MM/YYYY format
    Returns: (is_valid, format_type, datetime_object)
    """
    if not isinstance(date_string, str):
        return False,False

    # Pattern for YYYY-MM-DD
    iso_pattern = r'^\d{4}-\d{2}-\d{2}$'

    # Pattern for DD/MM/YYYY
    eu_pattern = r'^\d{2}/\d{2}/\d{4}$'
    if date_string == "":
      return False,False
    elif re.match(iso_pattern, date_string):
      return True,False
    elif re.match(eu_pattern, date_string):
        return True,True
    else:
        return False,False
    
def remove_whitespace(df):
  df = df.copy()
  columns_to_clean = df.select_dtypes(include=['object', 'string']).columns.tolist()
  df[columns_to_clean] = df[columns_to_clean].apply(lambda x: x.str.replace(" ", ""))
  return df

def normalize_date(df,column_name):
  df = df.copy()
  for idx in df.index:
    if (validate_date_format(df.loc[idx,column_name])[1] == True):
      if isinstance(df.loc[idx,column_name], str):
        day, month, year = df.loc[idx,column_name].split('/')
        df.loc[idx,column_name] = f"{year}-{month}-{day}"
  return df

def invalid_currency(df,column_name):
  df = df.copy()
  for idx in df.index:
    if currency_val(df.loc[idx,"column_name"]) == False:
      df.loc[idx,"column_name"] = None
  return df

def replace_missing_with_none(df, columns):
    """
    Replace missing values (NaN, NaT, None, etc.) with None in one or more specified columns.
    
    Parameters:
        df (pd.DataFrame): Input DataFrame.
        columns (str or list of str): Column name or list of column names to process.
    
    Returns:
        pd.DataFrame: DataFrame with missing values in the specified column(s) replaced by None.
    """
    # Normalize input to always be a list
    if isinstance(columns, str):
        columns = [columns]
    elif not isinstance(columns, (list, tuple)):
        raise ValueError("`columns` must be a string or a list/tuple of strings.")
    
    # Validate that all columns exist
    missing_cols = [col for col in columns if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Column(s) not found in DataFrame: {missing_cols}")
    
    # Work on a copy to avoid modifying the original DataFrame
    df = df.copy()
    
    # Replace missing values with None in each specified column
    for col in columns:
        df[col] = df[col].where(pd.notna(df[col]), None)
    
    return df

def impute_merchant(df,column_name):
  df = df.copy()
  df[column_name] = df[column_name].fillna(df[column_name].mode()[0])
  return df
def test_impute_merchant():
  df = pd.read_csv("data/banking_transactions.csv")
  df = impute_merchant(df,"merchant_category")
  assert isinstance(df.loc[200,"merchant_category"],str) == True
def cleaning(df):
  df = df.copy()
  print("Removing whitespace .....")
  df = remove_whitespace(df)
  print("Whitespace removed")
  print("Normalizing date to YYYY-MM-DD ......")
  df = normalize_date(df,"transaction_date")
  df = normalize_date(df,"value_date")
  print("Date normalized to YYYY-MM-DD")
  print("Replacing missing numeric value with None .....")
  df = replace_missing_with_none(df, ["amount","risk_score"])
  print("Missing numeric value replaced with None .....")
  df = impute_merchant(df,"merchant_category")
  print("Impute merchant category")
  
  return df

 