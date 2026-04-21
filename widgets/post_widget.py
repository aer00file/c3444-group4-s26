from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, NumericProperty, BooleanProperty
from kivy.properties import ListProperty
from kivy.uix.button import Button

class PostItem(BoxLayout):
    username = StringProperty("")
    body = StringProperty("")
    timestamp = StringProperty("")
    likes = NumericProperty(0)
    post_id = StringProperty("")
    tags = ListProperty([])
    compact_mode = BooleanProperty(False)
    liked = BooleanProperty(False)

    def open_post(self):
        app = App.get_running_app()
        sm = app.root

        comment_screen = sm.get_screen("comment")

        comment_screen.post_data = {
            "post_id": self.post_id,
            "username": self.username,
            "body": self.body
        }

        sm.current = "comment"
    def like_post(self):
        from postDB import update_likes
        if hasattr(self, "liked") and self.liked:
            return

        self.likes += 1
        self.liked = True
        update_likes(self.post_id, self.likes)

    def load_tags(self):
        if "tags_buttons_container" not in self.ids:
            return

        container = self.ids.tags_buttons_container
        container.clear_widgets()

        for tag in self.tags:
            btn = Button(
                text=f"#{tag}",
                size_hint_x=None,
                width=80,
                background_normal='',
                background_color=(0.2, 0.6, 1, 1)
            )
            btn.bind(on_release=lambda instance, t=tag: self.tag_clicked(t))
            container.add_widget(btn)

    def tag_clicked(self, tag):
        app = App.get_running_app()
        sm = app.root

        main_screen = sm.get_screen("main")

        main_screen.apply_filter_on_enter = True  # prevent reload
        sm.current = "main"

        main_screen.ids.search_input.text = tag
        main_screen.search_posts(tag)

    def on_kv_post(self, base_widget):
        self.load_tags()

    def on_tags(self, instance, value):
        self.load_tags()