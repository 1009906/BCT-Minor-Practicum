def difference_in_minutes(datetime1, datetime2):
    if datetime1 > datetime2:
        datetime1, datetime2 = datetime2, datetime1
    difference = datetime2 - datetime1
    return difference.total_seconds() / 60