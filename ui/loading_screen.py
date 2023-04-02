import tkinter as tk
from tkinter import ttk

class LoadingScreen(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title('Processing...')
        self.geometry('300x100')
        self.resizable(False, False)

        self.progressbar = ttk.Progressbar(self, orient='horizontal', length=280, mode='indeterminate')
        self.progressbar.pack(pady=10)

        self.label = tk.Label(self, text='Processing your image...', font=('Helvetica', 12))
        self.label.pack()

        self.protocol('WM_DELETE_WINDOW', self.cancel_processing)

    def start_processing(self):
        self.progressbar.start()

    def stop_processing(self):
        self.progressbar.stop()
        self.destroy()

    def cancel_processing(self):
        # Implement this method if you want to allow the user to cancel the processing
        pass
