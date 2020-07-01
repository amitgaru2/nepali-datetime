import os

BASE_DIR = os.path.join(os.path.dirname(__file__))
CALENDAR_PATH = os.path.join(BASE_DIR, 'data', 'calendar_bs.csv')
REFERENCE_DATE_AD = {'year': 1918, 'month': 4, 'day': 13}
MINDATE = {'year': 1975, 'month': 1, 'day': 1}
MAXDATE = {'year': 2100, 'month': 12, 'day': 30}
