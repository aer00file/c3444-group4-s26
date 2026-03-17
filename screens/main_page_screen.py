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
from kivy.properties import NumericProperty
from kivy.lang import Builder
from postDB import get_posts, create_post, update_likes
from firebase_Auth import login_user, signUp
from datetime import datetime
from kivy.properties import BooleanProperty
from kivy.uix.screenmanager import Screen

class PostItem(BoxLayout):
    title = StringProperty("")
    username = StringProperty("")
    body = StringProperty("")
    timestamp = StringProperty("")
    likes = NumericProperty(0)
    post_id = StringProperty("")
    
    def like_post(self):
        self.likes += 1
        update_likes(self.post_id, self.likes)


class MainPage(Screen):
    #This function submits the current post information as a new object in the database
    #This is essentially my placeholder function that you could call if you wish to from the post creation screen.

    is_creating_post = BooleanProperty(False) #toggle for posting buttons
    def show_post_input(self):
        self.is_creating_post = True

    def hide_post_input(self):
        self.is_creating_post = False


    def submit_post(self):
        user_email = App.get_running_app().current_user_email #Use this last variable here as the email/username variable
        content = self.ids.post_input.text  # or wherever your text input is

        if not content.strip():
            return  # prevent empty posts

        create_post(user_email, content)
        self.ids.post_input.text = ""  # clear input
        self.hide_post_input()         # 👈 hide input
        self.load_posts()              # refresh feed
    
    def on_enter(self):
        self.load_posts()

    def load_posts(self):
        raw_posts = get_posts()

        posts = []
        if raw_posts:
            for post_id, value in raw_posts.items():

                #Safety check to ensure incomplete or corrupt data doesn't cause a crash
                if not isinstance(value, dict):
                    continue  # skip corrupted entries

                if "content" not in value:
                    continue  # skip incomplete posts

                timestamp = value.get("timeposted", 0)
                dt = datetime.fromtimestamp(timestamp)

                posts.append({
                    "post_id": post_id,
                    "username": value.get("user", "Unknown"),
                    "body": value.get("content", ""),
                    "timestamp": dt.strftime("%Y-%m-%d %H:%M"),
                    "raw_timestamp": timestamp,
                    "likes": value.get("likes", 0)
                })

        #Sort posts from newest to oldest
        posts.sort(key=lambda p: p["raw_timestamp"], reverse=True)

        self.ids.rv.data = posts
