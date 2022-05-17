import re

regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

def is_valid_email(email_address):
    if re.fullmatch(regex, email_address):
        return True
    else:
        return False


def is_valid_number(number):
    number = str(number)
    if (number.startswith('+7') and len(number) == 12) or (number.startswith('8') and len(number) == 11):
        return True
