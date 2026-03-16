from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
import mainpage, screen2, screen3

# hierarhy:
#   ScreensSample (App)
#   |- MyScreens (ScreenManager)
#      |- MyScreen1 (Screen)
#      |- MyScreen2 (Screen)
#      |- MyScreen3 (Screen)

class MyScreens(ScreenManager):
    def screen_manager_method(self):
        print('Hello from screen manager')

class ScreensSample(App):
    def app_method(self):
        print('Hello from app')

ScreensSample().run()