from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.metrics import dp
from postDB import getProfile, get_posts, updateBio
from datetime import datetime

class ProfileScreen(Screen):

    def on_enter(self):
        app = App.get_running_app()
        uid = app.current_user_uid
        email = app.current_user_email

        # Load profile data
        profile = getProfile(uid)
        if profile:
            self.ids.email_label.text = profile.get("email", "Unknown")
            self.ids.bio_label.text = profile.get("bio", "")
        else:
            self.ids.email_label.text = "Unknown"
            self.ids.bio_label.text = ""
            
        # Ensure edit mode is off when entering
        self.ids.bio_input.opacity = 0
        self.ids.bio_input.disabled = True
        self.ids.edit_button.text = "Edit Bio"
        # Load user's posts
        self.load_user_posts(email)
        
    def save_bio(self):
        app = App.get_running_app()
        uid = app.current_user_uid
        new_bio = self.ids.bio_input.text

        updateBio(uid, new_bio)

        # Update UI immediately
        self.ids.bio_label.text = new_bio
    
    def toggle_bio_edit(self):
        bio_input = self.ids.bio_input
        edit_button = self.ids.edit_button
        bio_label = self.ids.bio_label

        if edit_button.text == "Edit Bio":
            # Switch to edit mode
            bio_input.opacity = 1
            bio_input.height = dp(100)
            bio_input.disabled = False
            edit_button.text = "Save Bio"
        else:
            # Save mode
            new_bio = bio_input.text
            app = App.get_running_app()
            uid = app.current_user_uid

            updateBio(uid, new_bio)

            # Update UI
            bio_label.text = new_bio

            # Hide input again
            bio_input.opacity = 0
            bio_input.height = 0
            bio_input.disabled = True
            edit_button.text = "Edit Bio"

    def load_user_posts(self, email):
        raw_posts = get_posts()
        results = []

        if raw_posts:
            for post_id, value in raw_posts.items():
                if not isinstance(value, dict):
                    continue

                if value.get("user") == email:
                    timestamp = value.get("timeposted", 0)
                    dt = datetime.fromtimestamp(timestamp)

                    results.append({
                        "post_id": post_id,
                        "username": value.get("user", "Unknown"),
                        "body": value.get("content", ""),
                        "timestamp": dt.strftime("%Y-%m-%d %H:%M"),
                        "raw_timestamp": timestamp,
                        "likes": value.get("likes", 0)
                    })

        # Sort newest first
        results.sort(key=lambda p: p["raw_timestamp"], reverse=True)

        # Display in RV
        self.ids.rv.data = results
    def go_back(self):
        self.manager.current = "main"
