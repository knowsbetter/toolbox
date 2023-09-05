import os
from typing import cast
from dotenv import load_dotenv

load_dotenv()

DB_URL = cast(str, os.getenv('DB_URL'))