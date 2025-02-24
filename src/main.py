from app.ui import App
from app.database.Loader import Loader

if __name__ == "__main__":
    loader = Loader("doe@gmail.com", "password", True)
    loader.load_data()
    App()