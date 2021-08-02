from datetime import datetime, timedelta

offset = 0

# ------------------ [ get_in_date_format() ] ------------------ # 
        # Returns the date in MM/DD/YYYY format
def get_in_date_format(st):
    dt = st.split('/')
    d = {
        'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04',
        'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08', 'Sep': '09',
        'Oct': '10', 'Nov': '11', 'Dec': '12'}
    month = d[dt[0]]
    return month + '/' + '/'.join(dt[1:])

# ------------------ [ current_date() ] ------------------ # 
        # Returns the current date in "MM/DD/YYYY HH:MM" format
def current_date():
    dt = datetime.now()
    dt += timedelta(hours = offset)
    return str(dt.month) + '/' + str(dt.day) + '/' + str(dt.year) + ' ' + str(dt.hour) + ':' + str(dt.minute)

# ------------------------------------ { User } ------------------------------------ # 
class MyDate():
    month, day, year = int(), int(), int()
    hour, minute = int(), int()

    # ------------------ [ days_in_month() ] ------------------ # 
        # Returns how many days in the date's month
    def days_in_month(self):
        if (self.month == 2):
            if (self.year % 4 == 0 and self.year % 100 != 0): return 29
            if (self.year % 400 == 0): return 29
            return 28
        if (self.month in [4, 6, 9, 11]): return 30
        return 31
 
    # ------------------ [ __init__() ] ------------------ # 
        # Initializes "month", "day", "year", "hour", "minute" to the current date and time
    def __init__(self, st = current_date()):
        _date = [int(x) for x in st.split(' ')[0].split('/')]
        _time = [int(x) for x in st.split(' ')[1].split(':')[:2]]

        self.month, self.day, self.year = _date[0], _date[1], _date[2]
        self.hour, self.minute = _time[0], _time[1]
    
    # ------------------ [ is_valid() ] ------------------ # 
        # Checks if the "month", "day" and "year" are within calendar limits
        # Checks if the date has passed or is too far ahead and returns false, otherwise true
        # Throws an exception if an error occurs while running, returns false by default
    def is_valid(self):
        try:
            if not (1 <= self.month <= 12): return False
            if not (1 <= self.day <= 31): return False
            if not (2021 <= self.year): return False

            if (self.day > self.days_in_month()): return False

            if not (0 <= self.hour <= 23): return False
            if not (0 <= self.minute <= 59): return False

            today = MyDate()

            if (self.year < today.year or self.year > today.year + 1): return False
            if (self.year == today.year and self.month < today.month): return False
            if (self.year == today.year and self.month == today.month and self.day < today.day): return False

            is_today = (self.year == today.year and self.month == today.month and self.day == today.day)
            if (is_today and self.hour < today.hour): return False
            if (is_today and self.hour == today.hour and self.minute < today.minute): return False

            return True
        except Exception: return False

    # ------------------ [ add() ] ------------------ # 
        # Adds the "duration" in hours to the date
    def add(self, duration):
        _datetime = datetime(self.year, self.month, self.day, self.hour, self.minute)
        _datetime += timedelta(hours = duration)

        _date = [int(x) for x in str(_datetime).split(' ')[0].split('-')]
        self.year, self.month, self.day = _datetime[0], _datetime[1], _datetime[2]
        
        _time = [int(x) for x in str(_datetime).split(' ')[1].split(':')[:2]]
        self.hour, self.minute = _time[0], _time[1]

        return str(self)

    # ------------------ [ delta() ] ------------------ # 
        # Retuns the number of minutes between the current and given date and time
    def delta(self):
        _datetime = datetime(self.year, self.month, self.day, self.hour, self.minute)
        current_date = datetime.now()
        current_date += timedelta(hours = offset)
        return int((_datetime - current_date).total_seconds() / 60)

    # ------------------ [ __lt__() ] ------------------ # 
        # Overloads the < operator to compare two dates with each other
    def __lt__(self, date2):
        _datetime1 = datetime(self.year, self.month, self.day, self.hour, self.minute)
        _datetime2 = datetime(date2.year, date2.month, date2.day, date2.hour, date2.minute)
        return (int((_datetime1 - _datetime2).total_seconds() / 60) < 0)

    # ------------------ [ __str__() ] ------------------ # 
        # Returns the string representation of the given date in "MM/DD/YYYY HH:MM" format
    def __str__(self):
        _month, _day, _year = str(self.month), str(self.day), str(self.year)
        _hour, _minute = str(self.hour), str(self.minute)
        if (self.month < 10): _month = "0" + _month
        if (self.day < 10): _day = "0" + _day
        if (self.hour < 10): _hour = "0" + _hour
        if (self.minute < 10): _minute = "0" + _minute
        return _month + "/" + _day + "/" + _year + " " + _hour + ":" + _minute

    # ------------------ [ footer() ] ------------------ # 
        # Returns the date and time in "MM/DD/YYYY at HH:MM" format
    def footer(self): return str(self).split()[0] + ' at ' + str(self).split()[1]

    def __eq__(self, date2):
        return (date2.month == self.month
                and date2.day == self.day
                and date2.year == self.year
                and date2.hour == self.hour
                and date2.minute == self.minute)