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

Builder.load_file('buddyupMainPage.kv')

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


class MainPage(Widget):
    #This function submits the current post information as a new object in the database
    #This is essentially my placeholder function that you could call if you wish to from the post creation screen.
    def submit_post(self):
        user_email = App.get_running_app().current_user_email #Use this last variable here as the email/username variable
        content = self.ids.post_input.text  # or wherever your text input is

        create_post(user_email, content)
        self.load_posts()  # refresh the feed
    
    def on_kv_post(self, base_widget):
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
                    "likes": value.get("likes", 0)
                })

        #Sort posts from newest to oldest
        posts.sort(key=lambda p: p["timestamp"], reverse=True)

        self.ids.rv.data = posts

class BuddyUpApp(App):
    def build(self):
        #This is a test variable to test the post creation function here.
        self.current_user_email = "tempuser"
        return MainPage()



if __name__ == '__main__':
    BuddyUpApp().run()