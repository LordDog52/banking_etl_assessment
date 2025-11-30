import pandas as pd
from validator import data_validation
from cleaner import cleaning
from transformer import transform
def load_csv(path: str) -> list[dict]:
  df = pd.read_csv(path)

  # Mandatory columns
  mandatory_columns = ["transaction_id","transaction_date","customer_id","account_id","amount","currency"]

  print("Checking empty row and missing column\n")

  # Check is row empty or mandatory columns missing
  for idx in df.index:
    if (df.loc[idx, df.columns[1:]].isnull().all() == True):
      print(f'Transaction with id {df.loc[idx, df.columns[0]]} is empty')
    elif (df.loc[idx, mandatory_columns].isnull().any() == True):
      print(f'Transaction with id {df.loc[idx, df.columns[0]]} missing mandatory columns')

  print("\nValidating Data\n")

  data_validation(df)
  print("\nValidation Completed")
  print("\nCleaning Data\n")
  df = cleaning(df)
  print("\nCleaning Completed\n")
  print("Transform data\n")
  df = transform(df)
  print("Data transformed\n")
  # Return dictionary
  list_of_dicts = df.to_dict(orient='records')
  return list_of_dicts