from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty
)

class MainPage(Widget):
        pass

class BuddyUpApp(App):
    def build(self):
        return MainPage()

if __name__ == '__main__':
    BuddyUpApp().run()
         