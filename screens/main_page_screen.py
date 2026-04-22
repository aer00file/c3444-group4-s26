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
from postDB import get_posts, create_post, update_likes, delete_post
from firebase_Auth import login_user, signUp
from datetime import datetime
from kivy.properties import BooleanProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

class MainPage(Screen):
    #This function submits the current post information as a new object in the database
    #This is essentially my placeholder function that you could call if you wish to from the post creation screen.

    is_creating_post = BooleanProperty(False) #toggle for posting buttons
    apply_filter_on_enter = BooleanProperty(False)
    def show_post_input(self, *args):
        container = self.ids.bottom_container
        container.clear_widgets()

        # MAIN vertical layout
        main_layout = BoxLayout(
            orientation='vertical',
            spacing=8,
            size_hint_y=None
        )

        # --- Post input ---
        self.input = TextInput(
            hint_text="Write a post...",
            multiline=False,
            size_hint_y=None,
            height=40
        )

        # --- Tags input ---
        self.tags_input = TextInput(
            hint_text="Enter tags (comma separated. Maximum of 3)",
            multiline=False,
            size_hint_y=None,
            height=40
        )

        self.input.bind(on_text_validate=lambda x: self.submit_post())

        # --- Buttons row ---
        button_row = BoxLayout(
            size_hint_y=None,
            height=40,
            spacing=10
        )

        send_btn = Button(
            text="Send",
            background_normal='',
            background_color=(0, 0.36, 0.02, 1)
        )
        send_btn.bind(on_press=self.submit_post)

        cancel_btn = Button(
            text="Cancel",
            background_normal='',
            background_color=(0.3, 0.3, 0.3, 1)
        )
        cancel_btn.bind(on_press=self.hide_post_input)

        button_row.add_widget(send_btn)
        button_row.add_widget(cancel_btn)

        # --- Add everything ---
        main_layout.add_widget(self.input)
        main_layout.add_widget(self.tags_input)
        main_layout.add_widget(button_row)

        container.add_widget(main_layout)


    def hide_post_input(self, *args):
        container = self.ids.bottom_container
        container.clear_widgets()

        post_btn = Button(
            text="📫 Post",
            font_name="EmojiFont",
            background_normal='',
            background_color=(0, 0.36, 0.02, 1)
        )
        post_btn.bind(on_press=self.show_post_input)

        profile_btn = Button(
            text="👤 Profile",
            font_name="EmojiFont",
            background_normal='',
            background_color=(0.2, 0.2, 0.2, 1)
        )
        profile_btn.bind(on_press=self.go_to_profile)

        container.add_widget(post_btn)
        container.add_widget(profile_btn)

    def go_to_profile(self, *args):
        self.manager.current = "profile"

    def submit_post(self, *args):
        print("SUBMIT CLICKED")

        user_email = App.get_running_app().current_user_email
        content = self.input.text.strip()

        if not content:
            return

        raw_tags = self.tags_input.text if hasattr(self, "tags_input") else ""

        tags = []
        if raw_tags:
            tags = [t.strip().lower() for t in raw_tags.split(",") if t.strip()]
            tags = list(dict.fromkeys(tags))
            tags = tags[:3]

        create_post(user_email, content, tags)

        self.tags_input.text = ", ".join(tags)      # clear dynamic input
        self.hide_post_input()    # restore buttons
        self.load_posts()         # refresh feed
    
    def on_enter(self):
        if not self.apply_filter_on_enter:
            self.load_posts()
        else:
            self.apply_filter_on_enter = False

        self.hide_post_input()

    def load_posts(self):
        self.ids.rv.data = []

        raw_posts = get_posts()

        posts = []
        if raw_posts:
            for post_id, value in raw_posts.items():

                if not isinstance(value, dict):
                    continue

                if "content" not in value:
                    continue

                timestamp = value.get("timeposted", 0)
                dt = datetime.fromtimestamp(timestamp)

                posts.append({
                    "post_id": post_id,
                    "username": value.get("user", "Unknown"),
                    "body": value.get("content", ""),
                    "timestamp": dt.strftime("%Y-%m-%d %H:%M"),
                    "raw_timestamp": timestamp,
                    "likes": value.get("likes", 0),
                    "tags": value.get("tags", [])
                })

        posts.sort(key=lambda p: p["raw_timestamp"], reverse=True)

        self.ids.rv.data = posts

    def search_posts(self, query, category="all"):
        """
        Search function that filters posts based on the query and category.
        - query: text typed into the search bar
        - category: "all", "content", or "user"
        """

        query = query.lower().strip()

        # Reset the full feed if the search value is empty
        if not query:
            self.load_posts()
            return

        raw_posts = get_posts()
        results = []  # Results is for the values that match the search

        for post_id, value in raw_posts.items():

            # Safe guard against any corrupted posts
            if not isinstance(value, dict):
                continue

            # Bring everything to lowercase so searches are not case sensitive
            content = value.get("content", "").lower()
            user = value.get("user", "").lower()
            tags = [t.lower() for t in value.get("tags", [])]

            match = False

            # These cover different cases of what part of the post we want to search specifically


            if category == "all":
                match = (
                        query in content or
                        query in user or
                        any(query in tag for tag in tags)
                )

            elif category == "content":
                match = query in content

            elif category == "user":
                match = query in user

            # Based off of a substring match (Eg: "dog" gives "dog" and "hotdog")
            if match:
                timestamp = value.get("timeposted", 0)
                dt = datetime.fromtimestamp(timestamp)

                # Adds the post to results
                results.append({
                    "post_id": post_id,
                    "username": value.get("user", "Unknown"),
                    "body": value.get("content", ""),
                    "timestamp": dt.strftime("%Y-%m-%d %H:%M"),
                    "raw_timestamp": timestamp,
                    "likes": value.get("likes", 0),
                    "tags": value.get("tags", [])
                })

        # Sort results newest to oldest
        results.sort(key=lambda p: p["raw_timestamp"], reverse=True)
        self.ids.rv.data = results
