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

def test_account_type_val():
  assert account_type_val("CREDIT_CARD") == True

