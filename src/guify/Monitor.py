import eel


class Monitor:
    def __init__(self):
        self.text = ''

    def set_text(self, text):
        eel.set_text(text)

    def write(self, text):
        self.text += str(text)
        eel.set_text(self.text)

    def clear_text(self):
        self.text = ""
        eel.set_text(self.text)
