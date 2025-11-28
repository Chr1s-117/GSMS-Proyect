# test_env.py (crear en raíz del proyecto)
from dotenv import load_dotenv
import os

load_dotenv()

print("=== VARIABLES DE ENTORNO ===")
print(f"DATABASE_URL: {os.getenv('DATABASE_URL')}")
print(f"UDP_PORT: {os.getenv('UDP_PORT')}")
print(f"ROOT_PATH: '{os.getenv('ROOT_PATH')}'")
print(f"HTTP_ALLOWED_ORIGINS: {os.getenv('HTTP_ALLOWED_ORIGINS')}")
print(f"WS_ALLOWED_ORIGINS: {os.getenv('WS_ALLOWED_ORIGINS')}")