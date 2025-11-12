#
# validators.py
#
# Entry field validators for the pytock application.
#

import re
import restaurant


# validate_name
#
# Ensure that the name is at least reasonable, returning <error>, <name>.
#
def validate_name(text):
    # Remove punctuation
    text = re.sub(r"[^\w\s]", "", text)
    # Remove extra whitespace
    text = re.sub(r"\s+", " ", text).strip()

    if len(text) == 0:
        return "Invalid Name", None
    else:
        return None, text


# validate_phone
#
# Ensure the phone number is valid, returning <error>, <phone>.
#
def validate_phone(phone):
    # Remove non-number stuff
    phone = re.sub(r"[^+\(\)\-\d\s]", "", phone)
    # Remove extra whitespace
    phone = re.sub(r"\s+", " ", phone).strip()

    if len(phone) == 0:
        return "Invalid Phone", None
    else:
        return None, phone


# validate_timeOfDay
#
# Ensure the time of day is valid, returning <error>, <timeOfDay>.
#
def validate_timeOfDay(timeOfDay):
    if not timeOfDay:
        return "Invalid Time of Day", None
    else:
        return None, timeOfDay


# validate_timePeriod
#
# Ensure the time period is valid, returning <error>, <timePeriod>.
#
def validate_timePeriod(timePeriod):
    maxBookTime = restaurant.Booking.maxBookingTime()
    if timePeriod > maxBookTime:
        return f"Maximum Booking Period is {maxBookTime.strftime("%H:%M")}", None
    else:
        return None, timePeriod


# validate_tablename
#
# Ensure the table name string is valid, returning <error>, <table>.
#
def validate_tablename(tablename):
    if len(tablename) == 0:
        return "Table Choice Required", None
    else:
        return None, tablename


# validate_seats
#
# Ensure the seat count is valid, returning <error>, <seats>.
#
def validate_seats(seats):
    if seats < 1 or seats > restaurant.Tables.MAX_SEATS:
        return f"Seats must be in the range 1..{restaurant.Tables.MAX_SEATS}", None
    else:
        return None, seats
