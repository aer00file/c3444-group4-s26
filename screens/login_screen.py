from kivy.uix.screenmanager import Screen

class LoginScreen(Screen):

    def login(self):
        username = self.ids.username.text
        password = self.ids.password.text

        # Example authentication logic
        if username == "admin" and password == "1234":
            self.manager.current = "post"   # switch to post screen
        else:
            self.ids.message.text = "Invalid username or password"