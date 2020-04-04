import tkinter as tk
from starcraft_replay_scanner import SC2Scanner
import sys

class Run_GUI():
	def __init__(self, parent, delay):
		self.parent = parent
		self.root = tk.Tk()
		self.root.title("Starcraft Replay Scanner")

		self.c_width = 600
		self.c_height = 400
		self.canvas = tk.Canvas(self.root, width=self.c_width, height=self.c_height)

		self.message = tk.Label(self.root, text='Starcraft Replay Scanner Running', fg='green')
		self.message.config(font=('Arial', 20))

		self.close_help = tk.Label(self.root, text="Hit END to end program")
		self.close_help.config(font=('Arial', 11))

		self.notice = tk.Label(self.root, text="For best experience don't END while daemon is running")
		self.notice.config(font=('Arial', 11))

		self.end_button = tk.Button (self.root, text='END',command=self.end, font=('Arial', 11, 'bold'))

		self.background_thread = SC2Scanner(delay) 
		

	def start(self):
		self.canvas.pack()
		self.canvas.create_window(300, 50, window=self.message)
		self.canvas.create_window(300, 150, window=self.close_help) 
		self.canvas.create_window(300, 250, window=self.notice)
		self.canvas.create_window(300, 350, window=self.end_button)

		self.background_thread.start()
		self.root.mainloop()

	def end(self):
		self.root.destroy()
		sys.exit()
