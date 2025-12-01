import pandas as pd
import datetime
import numpy

def date_conversion(df,column_name):
  df = df.copy()
  #df = normalize_date(df,column_name)
  df[column_name] = pd.to_datetime(df[column_name]).dt.date
  return df
def test_date_conversion():
  df = pd.read_csv("data/banking_transactions.csv")
  type(date_conversion(df[0:10],"transaction_date").loc[0,"transaction_date"]) == datetime.date

def convert_to_float(df,column_name):
  df = df.copy()
  df[column_name] = df[column_name].astype('float64')
  return df
def test_convert_to_float():
  df = pd.read_csv("data/banking_transactions.csv")
  assert type(convert_to_float(df[0:10],"amount").loc[0,"amount"]) == numpy.float64

