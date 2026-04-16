from kivy.uix.screenmanager import Screen
from kivy.app import App
from firebase_Auth import login_user, signUp

class LoginScreen(Screen):

    def login(self):
        username = self.ids.username.text
        password = self.ids.password.text

        success = login_user(username, password)

        if success:
            App.get_running_app().current_user_email = username
            self.manager.current_user = username

            # switch screens
            self.manager.current = "main"
        else:
            self.ids.message.text = "Invalid username or password"

    def sign_up(self):
        username= self.ids.username.text
        password = self.ids.password.text

        success = signUp(username, password)

        if success:
            App.get_running_app().current_user_email = username
            self.manager.current_user = username

            # switch screens
            self.manager.current = "main"
        else:
            self.ids.message.text = "Invalid username or password"
