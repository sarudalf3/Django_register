from datetime import date

def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

# Driver code
print(calculate_age(date(1981, 2, 17)), "years")