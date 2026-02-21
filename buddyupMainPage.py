from turtle import width
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Rectangle, Color
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder

Builder.load_file('buddyupMainPage.kv')

class MainPage(Widget):
    pass
    # name = ObjectProperty(None)
    # password = ObjectProperty(None)
    # #create press function
    # def press(self):
    #     name = self.ids.name.text
    #     password = self.ids.password.text

    #     #print(f'Hello {name}, your password is {password}')
    #     #Prints to the terminal, but we want to print to the app
    #     #self.add_widget(Label(text=f'Hello {name}, your password is {password}'))
    #     print(f'Hello {name}, your password is {password}')
    #     #clear the text input
    #     self.ids.name.text = ""
    #     self.ids.password.text = ""

class BuddyUpApp(App):
    def build(self):
        return MainPage()


if __name__ == '__main__':
    BuddyUpApp().run()