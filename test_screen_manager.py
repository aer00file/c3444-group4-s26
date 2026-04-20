from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder

# Load Widget files
Builder.load_file("widgets/mainpage_widget.kv")
Builder.load_file("widgets/login_widget.kv")
Builder.load_file("widgets/profile_widget.kv")

# Import screens
from screens.main_page_screen import MainPage
from screens.login_screen import LoginScreen
from screens.profile_screen import ProfileScreen

# Actual Testing Logic
class TestApp(App):
    def build(self):
        self.current_user_email = "tempuser"
        sm = ScreenManager()

        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(MainPage(name="main"))
        sm.add_widget(ProfileScreen(name="profile"))

        sm.current = "login"

        return sm

if __name__ == "__main__":
    TestApp().run()
