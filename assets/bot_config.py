from os import getenv
from dotenv import load_dotenv

load_dotenv()

api_key = getenv("API_TOKEN")
admin_ids = getenv("ADMIN_IDS")
website_url = getenv("WEBSITE_URL")