import re
def check_txn_pattern_regex(text):
    """Check if string matches TXN followed by exactly 7 digits"""
    pattern = r'^TXN\d{7}$'
    return bool(re.match(pattern, text))
def test_txn_pattern_regex():
  assert check_txn_pattern_regex("TXN0139413") == True

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

def test_validate_date_format():
  assert validate_date_format("12/04/1900") == (True,True)

def amount_val(amount):
  return (0 < amount <= 10000000)
def test_amount_val():
  assert amount_val(-1) == False
def currency_val(currency):
  return currency in ["IDR", "USD", "SGD"]
def test_currency_val():
  assert currency_val("USD") == True
def direction_val(direction):
  return direction in ["DEBIT", "CREDIT"]
def test_direction_val():
  assert direction_val("DEBUT") == False
def account_type_val(account_type):
  return account_type in ["SAVINGS", "CURRENT", "CREDIT_CARD", "LOAN"]
def account_type_val():
  assert account_type_val("CREDIT_CARD") == True
def data_validation(df):
  for idx in df.index:

    # transaction_id wajib mengikuti pola: TXNxxxxxxx
    if (check_txn_pattern_regex(df.loc[idx,"transaction_id"]) == False):
      print(f'for id {df.loc[idx, df.columns[0]]} transaction id is invalid must use pattern TXNxxxxxxx')

    # Tanggal harus valid (deteksi format YYYY-MM-DD dan DD/MM/YYYY)
    if (validate_date_format(df.loc[idx,"transaction_date"])[0] == False):
      print(f'for id {df.loc[idx, df.columns[0]]} transaction date is invalid must use pattern YYYY-MM-DD or DD/MM/YYYY')

    if (validate_date_format(df.loc[idx,"value_date"])[0] == False):
      print(f'for id {df.loc[idx, df.columns[0]]} value date is invalid must use pattern YYYY-MM-DD or DD/MM/YYYY')

    # amount tidak boleh: bernilai negatif, kosong, dan lebih besar dari 10.000.000 IDR (flag anomaly)
    if amount_val(df.loc[idx, "amount"]) == False:
      print(f'for id {df.loc[idx, df.columns[0]]} amount is invalid must not negative, zero, and bigger than 10.000.000 IDR')

    # currency harus salah satu dari: IDR, USD, dan SGD
    if currency_val(df.loc[idx, "currency"]) == False:
      print(f'for id {df.loc[idx, df.columns[0]]} currency is invalid must use IDR, USD or SGD')

    # direction harus DEBIT atau CREDIT
    if direction_val(df.loc[idx, "direction"]) == False:
      print(f'for id {df.loc[idx, df.columns[0]]} direction is invalid must use DEBIT or CREDIT')

    # account_type harus salah satu dari: SAVINGS, CURRENT, CREDIT_CARD, LOAN
    if account_type_val(df.loc[idx, "account_type"]) == False:
      print(f'for id {df.loc[idx, df.columns[0]]} account type is invalid must use SAVINGS, CURRENT, CREDIT_CARD, or LOAN')
