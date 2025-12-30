from datetime import datetime

def parse_dob(text):
    try:
        d = datetime.strptime(text, "%d/%m/%Y")
        if 1950 <= d.year <= 2020:
            return text
    except:
        pass
    return ""
