import eel


class Monitor:
    def __init__(self):
        self.text = ''

    def set_text(self, text):
        '''
        Replace all text in monitor to "text".
        :param text: The text to replace the monitor text with.
        '''
        self.text = str(text)
        eel.set_monitor_text(self.text)

    def write(self, text):
        '''
        Add text to the monitor.
        :param text: The text to add to the monitor.
        '''
        self.text += str(text)
        eel.set_monitor_text(self.text)

    def flush(self):
        '''
        Clear the monitor.
        '''
        self.text = ""
        eel.set_monitor_text(self.text)
