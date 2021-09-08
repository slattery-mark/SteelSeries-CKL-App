from tkinter import Tk, ttk, Frame
from threading import Event, Thread

from engine_app import CKL

class tkinterApp(Tk):
    def __init__(self):
        super().__init__()
        
        self.title('CKL')
        self.resizable(0,0)

        self.ckl = CKL()
        self.kill_switch = Event()
        self.threads = []
        self.frames = {} 

        container = Frame(self)
        container.pack(padx=12, pady=12)

        for i in (Page1, Page2):
            frame = i(container, self)
            self.frames[i] = frame
            frame.grid(row=1, column=0, sticky="nsew")
  
        self.show_frame(Page1)
  
    def registerGame(self):
        """Calls the CKL method to register this application to Engine."""
        self.ckl.registerGame()
        self.ckl.bindGameEvent()

    def removeGame(self):
        """Calls the CKL method to remove this application from Engine."""
        self.ckl.removeGameEvent()
        self.ckl.removeGame()

    def show_frame(self, page):
        """Moves a frame of the GUI to the top for display."""
        frame = self.frames[page]
        frame.tkraise()
    
    def start(self):
        """Spins a thread to send lighting events."""
        thread = Thread(target=self.ckl.sendGameEvent, args=(0, self.kill_switch))
        self.threads.append(thread)
        thread.start()

    def stop(self):
        """Kills any active threads."""
        self.kill_switch.set()
        for thread in self.threads:
            thread.join()
            self.threads.remove(thread)
        self.kill_switch.clear()

class Page1(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        # duplicate widgets
        btnStartStop = ttk.Button(self, text='Start/Stop', width=15, state='disabled', command=lambda:controller.show_frame(Page1))
        btnRegistration = ttk.Button(self, text ='Registration', width=15, command=lambda:controller.show_frame(Page2))
        label = ttk.Label(self, text='Start/Stop', font='bold')

        btnStartStop.grid(row=1, column=0, ipady=3, pady=(0,7))
        btnRegistration.grid(row=1, column=1, ipady=3, pady=(0,7))
        label.grid(row=0, column=0, columnspan=2, pady=(0,10))

        # page specific
        btnStart = ttk.Button(self, text='Start', width=32, command=lambda:[btnStart.state(['disabled']), btnStop.state(['!disabled']), controller.start()])
        btnStop = ttk.Button(self, text='Stop', width=32, state='disabled', command=lambda:[btnStop.state(['disabled']), btnStart.state(['!disabled']), controller.stop()])

        btnStart.grid(row=2, column=0, columnspan=2, pady=(5,0), ipady=5)
        btnStop.grid(row=3, column=0, columnspan=2, pady=(5,0), ipady=5)    
  
class Page2(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        # duplicate widgets
        btnStartStop = ttk.Button(self, text ='Start/Stop', width='15', command=lambda:controller.show_frame(Page1))
        btnRegistration = ttk.Button(self, text ='Registration', width='15', state='disabled', command=lambda:controller.show_frame(Page2))
        label = ttk.Label(self, text='Registration', font='bold')

        btnStartStop.grid(row=1, column=0, ipady=3, pady=(0,7))
        btnRegistration.grid(row=1, column=1, ipady=3, pady=(0,7))
        label.grid(row=0, column=0, columnspan=2, pady=(0,10))

        # page specific
        btnRegister = ttk.Button(self, text='Register', width=32, state='disabled', command=lambda:[btnRegister.state(['disabled']), btnDeregister.state(['!disabled']), controller.registerGame()])
        btnDeregister = ttk.Button(self, text='Deregister', width=32, command=lambda:[btnDeregister.state(['disabled']), btnRegister.state(['!disabled']), controller.removeGame()])

        btnRegister.grid(row=2, column=0, columnspan=2, pady=(5,0), ipady=5)
        btnDeregister.grid(row=3, column=0, columnspan=2, pady=(5,0), ipady=5)

if __name__ == "__main__":
    gui = tkinterApp()
    gui.mainloop()
    gui.stop()
