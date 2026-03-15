from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, NumericProperty

class PostWidget(BoxLayout):
    username = StringProperty("")
    body = StringProperty("")
    likes = NumericProperty(0)

    def like_post(self):
        self.likes += 1