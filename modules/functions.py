#!/usr/bin/python
# packages
import re
import math
import pytz
import datetime
import data


def get_day_month_year_from_date(date):
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

    date_parts = date.split()
    french_month = date_parts[2].lower()

    if french_month in months:
        # extract numbers in day part
        day_number = re.findall(data.regex_number, date_parts[1])[0]
        month_number = months[french_month]
        year = date_parts[3]
        print("day_number", day_number)
        print("month_number", month_number)
        print("year", year)
        return day_number, month_number, year
    else:
        raise ValueError(f"KO : The provided French month '{french_month}' does not exist")


def extract_start_and_end_time(time: str):
    try:
        # Check if time is a string
        if not isinstance(time, str):
            raise ValueError("Input should be a string")
        pattern = r'\d{2}h\d{2}'
        matches = re.findall(pattern, time)
        if len(matches) >= 2:
            start_hour = matches[0]
            end_hour = matches[1]
            print("start_hour", start_hour)
            print("end_hour", end_hour)
            return start_hour, end_hour
        else:
            raise ValueError("No matching start and end times found")
    except Exception as e:
        return f"Error: {str(e)}"


def get_hours_and_minutes(clock_elements: str):
    try:
        if not isinstance(clock_elements, str):
            raise ValueError("Input should be a string")
        pattern = r'(\d{2})h(\d{2})'
        match = re.search(pattern, clock_elements)

        if match:
            hours = int(match.group(1))
            minutes = int(match.group(2))
            print("Hours:", hours)
            print("Minutes:", minutes)
            return hours, minutes
        else:
            raise ValueError("No valid time format found in the string")
    except Exception as e:
        return f"Error: {str(e)}"


def date_converter_french_date_to_utc_timestamp(french_date: str):
    try:
        day, month, year = get_day_month_year_from_date(french_date)
        formatted_date = f"{day}-{month}-{year}"
        dt_object = datetime.datetime.strptime(formatted_date, "%d-%m-%Y")
        utc_timestamp = dt_object.replace(tzinfo=pytz.UTC).timestamp()
        return utc_timestamp
    except ValueError as e:
        return f"KO: {str(e)}"


def add_clock_elements_to_utc_timestamp(utc_timestamp, clock_elements):
    try:
        if not isinstance(utc_timestamp, (int, float)):
            raise ValueError("utc_timestamp should be a numeric value")

        hours_to_add, minutes_to_add = get_hours_and_minutes(clock_elements)
        utc_datetime = datetime.datetime.utcfromtimestamp(utc_timestamp)
        new_datetime = utc_datetime + datetime.timedelta(hours=hours_to_add, minutes=minutes_to_add)
        new_utc_timestamp = new_datetime.replace(tzinfo=pytz.UTC).timestamp()
        return new_utc_timestamp
    except Exception as e:
        return f"Error: {str(e)}"


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
