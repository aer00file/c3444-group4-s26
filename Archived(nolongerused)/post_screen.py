from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from widgets.post_widget import PostWidget

class PostData:
    def __init__(self, username, body, image=None):
        self.username = username
        self.body = body
        self.image = image
        self.likes = 0
        self.comments = []

class PostScreen(Screen):

    def on_enter(self):
        if not hasattr(self, "initialized"):
            self.build_ui()
            self.initialized = True

    def build_ui(self):
        layout = BoxLayout(orientation="vertical")

        # Scroll feed
        self.feed = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.feed.bind(minimum_height=self.feed.setter("height"))

        scroll = ScrollView()
        scroll.add_widget(self.feed)

        # Create post section
        self.input_box = TextInput(hint_text="Type Here...",
                                   size_hint_y=None,
                                   height=100)

        post_button = Button(text="Post",
                             size_hint_y=None,
                             height=50)

        post_button.bind(on_release=self.create_post)

        layout.add_widget(scroll)
        layout.add_widget(self.input_box)
        layout.add_widget(post_button)

        self.add_widget(layout)


    def create_post(self, instance):
        text = self.input_box.text.strip()
        if text:
            post = PostWidget(username="You", body=text)
            self.feed.add_widget(post, index=0)
            self.input_box.text = ""