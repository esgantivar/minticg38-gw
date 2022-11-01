import os

from dotenv import load_dotenv
load_dotenv()

URL = os.environ.get("URL")
PORT = int(os.environ.get("PORT"))
URL_ACADEMIC = os.environ.get("URL_ACADEMIC")
URL_SECURITY = os.environ.get("URL_SECURITY")
JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")

