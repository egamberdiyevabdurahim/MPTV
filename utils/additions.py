import os
import pytz

from datetime import datetime


PATTERN = r"^\+?[\d\s]{10,15}$"

ADMIN_LINK = "@MasterPhoneAdmin"
ADMIN_EMAIL = "egamberdiyevabdurahim@gmail.com"

# Setting the base path
BASE_PATH = os.path.dirname(__file__)


# Set timezone to Asia/Tashkent
tashkent_timezone = pytz.timezone("Asia/Tashkent")
tashkent_time = datetime.now(tashkent_timezone)
