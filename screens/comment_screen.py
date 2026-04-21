from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.app import App
from datetime import datetime

from widgets.comment_widget import CommentWidget
from widgets.post_widget import PostItem
from postDB import get_comments, add_comment


class CommentScreen(Screen):
    post_data = {}

    def on_pre_enter(self):
        self.build_ui()
        self.load_comments()

    def build_ui(self):
        self.clear_widgets()

        layout = BoxLayout(
            orientation="vertical",
            spacing=10,
            padding=10
        )

        # ORIGINAL POST CARD
        self.post_card = PostItem(
            username=self.post_data["username"],
            body=self.post_data["body"],
            timestamp="",
            likes=0,
            post_id=self.post_data["post_id"],
            compact_mode=True,
            size_hint_y=None,
            height=170
        )
        layout.add_widget(self.post_card)

        # COMMENTS AREA
        self.comments_layout = GridLayout(
            cols=1,
            spacing=10,
            size_hint_y=None
        )
        self.comments_layout.bind(
            minimum_height=self.comments_layout.setter("height")
        )

        scroll = ScrollView()
        scroll.add_widget(self.comments_layout)

        layout.add_widget(scroll)

        # BOTTOM INPUT BAR
        bottom = BoxLayout(
            size_hint_y=None,
            height=55,
            spacing=8
        )

        self.input = TextInput(
            hint_text="Write a comment...",
            multiline=False
        )

        send_btn = Button(
            text="Send",
            size_hint_x=.22
        )
        send_btn.bind(on_release=self.submit_comment)

        cancel_btn = Button(
            text="Back",
            size_hint_x=.22
        )
        cancel_btn.bind(on_release=self.go_back)

        bottom.add_widget(self.input)
        bottom.add_widget(send_btn)
        bottom.add_widget(cancel_btn)

        layout.add_widget(bottom)

        self.add_widget(layout)

    def go_back(self, instance):
        self.manager.current = "main"

    def clear_input(self, instance):
        self.input.text = ""

    def load_comments(self):
        self.comments_layout.clear_widgets()

        comments = get_comments(self.post_data["post_id"])

        if comments:
            for cid, c in comments.items():
                if not isinstance(c, dict):
                    continue

                user = c.get("user", "Unknown")
                text = c.get("content", "")
                timestamp = c.get("timeposted", 0)

                dt = datetime.fromtimestamp(timestamp)

                widget = CommentWidget(
                    username=user,
                    text=text,
                    timestamp=dt.strftime("%m/%d %H:%M")
                )

                self.comments_layout.add_widget(widget)

    def submit_comment(self, instance):
        text = self.input.text.strip()

        if not text:
            return

        user = App.get_running_app().current_user_email

        add_comment(
            self.post_data["post_id"],
            user,
            text
        )

        self.input.text = ""
        self.load_comments()