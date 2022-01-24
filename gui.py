from tkinter import *
from chat import get_response

FONT = 'Abadi 11 bold'
FONT_BOLD = 'Abadi 11 bold'

bot_name = 'S.A.M'

class ChatAppApplication:

    def __init__(self):
        self.window = Tk()
        self._setup_main_window()

    def run(self):
        self.window.mainloop()

    def _setup_main_window(self):
        self.window.title('SWD Chatbot')
        self.window.resizable(width=False, height=False)
        self.window.configure(width=470, height=500, bg='#FDFEFE')

        head_label = Label(self.window, bg='#2E4053', fg='#FDFEFE', text='Stadtwerke Anfragen Manager', font=FONT_BOLD, pady=10)
        head_label.place(relwidth=1)

        # tiny divider
        line = Label(self.window, width=450, bg='#FDFEFE')
        line.place(relwidth=1, rely=0.07, relheight=0.012)

        # Text widget
        self.text_widget = Text(self.window, width=20, height=2, bg='#FDFEFE', fg='#17202A', font=FONT, padx=5, pady=5)
        self.text_widget.place(relheight=0.8, relwidth=1, rely=0.08)
        self.text_widget.configure(cursor="arrow", state=DISABLED)
        
        # Scroll bar
        scrollbar = Scrollbar(self.text_widget)
        scrollbar.place(relheight=1, relx=0.974)
        scrollbar.configure(command=self.text_widget.yview)

        # Bottom label 
        bottom_label = Label(self.window, bg='#FDFEFE', height=60)
        bottom_label.place(relwidth=1, rely=0.88)

        # Message entry box
        self.message = Entry(bottom_label, bg='#FDFEFE', fg='#17202A', font=FONT)
        self.message.place(relwidth=0.75, relheight=0.03, relx=0.008, rely=0.011)
        self.message.focus()
        self.message.bind('<Return>', self._on_enter_pressed)

        # Send button
        send_button = Button(bottom_label, text="Senden", font=FONT_BOLD, width=20, bg='#2E4053', fg='#FDFEFE',
                             command=lambda: self._on_enter_pressed(None))
        send_button.place(relx=0.77, rely=0.011, relheight=0.03, relwidth=0.22)


    def _on_enter_pressed(self, event):
        msg = self.message.get()
        self._insert_message(msg, 'Du')

    def _insert_message(self, msg, sender):
        if not msg: 
            return 

        self.message.delete(0, END)
        msg1 = f'{sender}: {msg}\n'
        self.text_widget.configure(cursor='arrow', state=NORMAL)
        self.text_widget.insert(END, msg1)
        self.text_widget.configure(cursor='arrow', state=DISABLED)

        msg2 = f'{bot_name}: {get_response({msg})}\n\n'
        self.text_widget.configure(cursor='arrow', state=NORMAL)
        self.text_widget.insert(END, msg2)
        self.text_widget.configure(cursor='arrow', state=DISABLED)

        self.text_widget.see(END)

if __name__ == '__main__':
    app = ChatAppApplication()
    app.run()