import os
from datetime import date, datetime

BLOCK_TIME = 2
EXA = 18
NOW = datetime.utcnow()
PROJECT_DIR = os.path.dirname(__file__)
TRACKER_API_ENDPOINT = "https://tracker.icon.community/api/v1"
YEAR = date.today().year
