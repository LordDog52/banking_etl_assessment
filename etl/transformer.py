import pandas as pd
def date_conversion(df,column_name):
  df = df.copy()
  #df = normalize_date(df,column_name)
  df[column_name] = pd.to_datetime(df[column_name]).dt.date
  return df

def convert_to_float(df,column_name):
  df = df.copy()
  df[column_name] = df[column_name].astype('float64')
  return df

def derived_feature(df):
  df = df.copy()

  df['is_large_transaction'] = pd.NA
  df['is_crossborder'] = pd.NA
  df['transaction_day'] = pd.NA
  for idx in df.index:
    if df.loc[idx,"amount"] > 5000000 and isinstance(df.loc[idx,"amount"],float):
      df.loc[idx,'is_large_transaction'] = True
    else:
      df.loc[idx,'is_large_transaction'] = False

    if df.loc[idx,"currency"] != 'IDR' and isinstance(df.loc[idx,"currency"],str):
      df.loc[idx,'is_crossborder'] = True
    else:
      df.loc[idx,'is_crossborder'] = False
    try:
      df.loc[idx,'transaction_day'] = df.loc[idx,'transaction_date'].strftime("%A")
    except ValueError:
      continue
    
  return df

def transform(df):
  df = df.copy()
  print("Transforming date ....")
  df = date_conversion(df,"transaction_date")
  df = date_conversion(df,"value_date")
  print("Date transformed into datetime.date ....")
  print("converting numeric value datatype into float")
  df = convert_to_float(df,"amount")
  df = convert_to_float(df,"risk_score")
  print("Numeric value datatype converted into float")
  print("deriving feature")
  df = derived_feature(df)
  return df