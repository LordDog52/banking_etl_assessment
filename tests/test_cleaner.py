import pandas as pd

def impute_merchant(df,column_name):
  df = df.copy()
  df[column_name] = df[column_name].fillna(df[column_name].mode()[0])
  return df

def test_impute_merchant():
  df = pd.read_csv("data/banking_transactions.csv")
  df = impute_merchant(df,"merchant_category")

    




 