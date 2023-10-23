#!/usr/bin/python
# packages
import re
import math
import pytz
import datetime
import data


def date_converter_french_date_to_utc_timestamp(french_date: str):
    months = {
        "janvier": "01",
        "fevrier": "02",
        "février": "02",
        "mars": "03",
        "avril": "04",
        "mai": "05",
        "juin": "06",
        "juillet": "07",
        "juil.": "07",
        "août": "08",
        "septembre": "09",
        "sept.": "09",
        "octobre": "10",
        "novembre": "11",
        "décembre": "12",
        "decembre": "12"
        }

    date_parts = french_date.split()
    french_month = date_parts[2].lower()

    if french_month in months:
        # extract numbers in day part
        day_number = re.findall(data.regex_number, date_parts[1])[0]
        month_number = months[french_month]
        print("day_number", day_number)
        print("month_number", month_number)
        print("year", date_parts[3])
        formatted_date = f"{day_number}-{month_number}-{date_parts[3]}"
        dt_object = datetime.datetime.strptime(formatted_date, "%d-%m-%Y")
        utc_timestamp = dt_object.replace(tzinfo=pytz.UTC).timestamp()
        return utc_timestamp
    else:
        print(f"KO : The provided French month '{french_month}' does not exist")
        return None


def get_department_name(department_number):
    try:
        department_name = data.department_names[department_number]
        return department_name
    except ValueError:
        print(f"KO : No department got the number {department_number}s")


def contains_numbers(input_string: str):
    pattern = r'\d+'
    return bool(re.search(pattern, input_string))


def are_timestamps_equal(timestamp1: float, timestamp2: float, tolerance_seconds=10):
    return math.isclose(timestamp1, timestamp2, abs_tol=tolerance_seconds)
