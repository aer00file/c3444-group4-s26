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
        self.hide_post_input()         # hide input
        self.load_posts()              # refresh feed
    
    def on_enter(self):
        self.load_posts()
    #Displays all valid posts within the database
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
        
    def search_posts(self, query, category="all"):
        query = query.lower().strip()
        #Reset the full feed if the search value is empty
        if not query:
            self.load_posts()
            return

        raw_posts = get_posts()
        #Results is for the values that match the search
        results = []

        for post_id, value in raw_posts.items():
            #Safe guard against any corrupted posts
            if not isinstance(value, dict):
                continue
            #Bring everything to lowercase so searches then are not case sensetive
            content = value.get("content", "").lower()
            user = value.get("user", "").lower()
            
            match = False

            #These cover just different cases of what part of the post we want to search specifically
            if category == "all":
                match = query in content or query in user

            elif category == "content":
                match = query in content
    
            elif category == "user":
                match = query in user
    
            elif category == "title":
                title = value.get("title", "").lower()
                match = query in title

            # Add more categories later if needed

            #Based off of a substring match (Eg: "dog" gives "dog" and "hotdog")
            if match:
                timestamp = value.get("timeposted", 0)
                dt = datetime.fromtimestamp(timestamp)
                #Adds the post to results
                results.append({
                    "post_id": post_id,
                    "username": value.get("user", "Unknown"),
                    "body": value.get("content", ""),
                    "timestamp": dt.strftime("%Y-%m-%d %H:%M"),
                    "raw_timestamp": timestamp,
                    "likes": value.get("likes", 0)
                })

        # Sort results newest to oldest
        results.sort(key=lambda p: p["raw_timestamp"], reverse=True)
        self.ids.rv.data = results
        
class BuddyUpApp(App):
    def build(self):
        #This is a test variable to test the post creation function here.
        self.current_user_email = "tempuser"
        return MainPage()



if __name__ == '__main__':
    BuddyUpApp().run()
