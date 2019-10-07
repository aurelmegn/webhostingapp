from datetime import datetime


def date_format_datetime(value, date_format="medium"):
    if date_format == "full":
        date_format = "%d, %b %Y"
    elif date_format == "medium":
        date_format = "%d, %b %Y"
        
    return date_format.format(value)
