from turtle import width
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import RoundedRectangle, Color, Rectangle
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.lang import Builder

Builder.load_file('buddyupMainPage.kv')

class PostItem(BoxLayout):
    title = StringProperty("")
    body = StringProperty("")

class MainPage(Widget):
    #placeholder values until database is complete
    def on_kv_post(self, base_widget):
        posts = [
            {"title": "Post 1", "body": "This is the first post."},
            {"title": "Post 2", "body": "Electric Boogaloo"},
            {"title": "Post 3", "body": "The quest for more data entries"}
        ]
        
        self.ids.rv.data = posts

class BuddyUpApp(App):
    def build(self):
        return MainPage()



if __name__ == '__main__':
    BuddyUpApp().run()
