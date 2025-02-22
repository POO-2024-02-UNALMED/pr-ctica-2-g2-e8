from app.ui import MainWindow
if __name__ == "__main__":
    window = MainWindow()
    window.run()

    # bad practice: it will execute only by importing
    # from app.ui import WelcomeWindow