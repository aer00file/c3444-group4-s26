from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty

class CommentWidget(BoxLayout):
    username = StringProperty("")
    text = StringProperty("")
    timestamp = StringProperty("")