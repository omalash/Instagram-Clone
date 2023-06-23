import re

# a valid password is at least 8 letters long, contains at least one lowercase and uppercase character,
# number, and special character

def is_valid_password(password):
    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#\$%\^&\*\(\)\.]).{8,}$"
    return bool(re.match(pattern, password))