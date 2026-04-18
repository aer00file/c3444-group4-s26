from kivy.uix.screenmanager import Screen
from kivy.app import App
from firebase_Auth import login_user, signUp
from postDB import createUserProfile

class LoginScreen(Screen):

    def login(self):
        email = self.ids.email.text
        password = self.ids.password.text

        result = login_user(email, password)

        # Firebase login success check
        if "localId" in result:
            uid = result["localId"]
            idToken = result["idToken"]

            # Store user info globally
            app = App.get_running_app()
            app.current_user_email = email
            app.current_user_uid = uid
            app.current_user_token = idToken

            # Switch screens
            self.manager.current = "main"

        else:
            # Show Firebase error message
            self.ids.message.text = "Invalid username or password"
    def signup(self):
        email = self.ids.username.text
        password = self.ids.password.text

        result = signUp(email, password)

        if "localId" in result:
            uid = result["localId"]
            idToken = result["idToken"]

            # Create user profile in database
            createUserProfile(uid, email)

            # Store user info globally
            app = App.get_running_app()
            app.current_user_email = email
            app.current_user_uid = uid
            app.current_user_token = idToken

            # Go to main screen
            self.manager.current = "main"
        else:
            error = result.get("error", {}).get("message", "Unknown error")
            self.ids.message.text = f"Sign up failed: {error}"
