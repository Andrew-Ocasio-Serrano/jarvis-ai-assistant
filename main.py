from app.cli import run
from config.settings import validate_config

if __name__ == "__main__":
    try:
        validate_config()
        run()
    except EnvironmentError as e:
        print(f"ERROR: {e}")