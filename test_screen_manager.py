from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder

# Load Widget files
Builder.load_file("widgets/post_widget.kv")
Builder.load_file("widgets/login_widget.kv")

# Import screens
from screens.post_screen import PostScreen
from screens.login_screen import LoginScreen

# Actual Testing Logic
class TestApp(App):
    def build(self):
        sm = ScreenManager()

        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(PostScreen(name="post"))

        sm.current = "login"

        return sm

if __name__ == "__main__":
    TestApp().run()