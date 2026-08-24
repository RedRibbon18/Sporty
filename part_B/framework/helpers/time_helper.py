from datetime import datetime, timedelta, timezone

def get_current_date_with_tz():
    return datetime.now().astimezone()

def get_next_day(today):
    return today + timedelta(days=1)

def get_dt_object_from_str_with_utc_tz(date_str, frmt):
    return datetime.strptime(date_str, frmt).replace(tzinfo=timezone.utc)