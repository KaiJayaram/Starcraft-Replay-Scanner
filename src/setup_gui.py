from tkinter.filedialog  import askdirectory, askopenfilename
import tkinter as tk
from pathlib import Path
import os.path
import starcraft_replay_scanner as SRS
from tkinter import messagebox

## GUI for Installer
class Setup_GUI():
	def __init__(self, config_file):
		self.root = tk.Tk()
		self.root.title("Starcraft Replay Scanner")

		self.home = str(Path.home())
		self.default_replay_dir = "{}\\Documents\\StarCraft II\\Accounts".format(self.home)
		self.default_replay_str = tk.StringVar()
		self.default_replay_str.set(self.default_replay_dir)
		self.default_output_loc = "starcraft_replay_scan.csv"
		self.default_output_str = tk.StringVar()
		self.default_output_str.set(self.default_output_loc)

		self.config_file = config_file

		self.c_width = 800
		self.c_height = 600
		self.canvas = tk.Canvas(self.root, width=self.c_width, height=self.c_height)

		self.title = tk.Label(self.root, text='Starcraft Replay Scanner')
		self.title.config(font=('Arial', 20))

		self.rep_help = tk.Label(self.root, text="Select Starcraft Accounts Directory")
		self.rep_help.config(font=('Arial', 11))

		self.out_help = tk.Label(self.root, text="Select output file name (csv)")
		self.out_help.config(font=('Arial', 11))


		self.name_help = tk.Label(self.root, text="Choose your SC2 Usernames (EX: user1,user2,user3...)")
		self.name_help.config(font=('Arial', 11))


		self.race_help = tk.Label(self.root, text="Choose your SC2 Races (EX: z,t,p)")
		self.race_help.config(font=('Arial', 11))

		# config entries
		self.dir_entry = tk.Entry (self.root, textvariable=self.default_replay_str, width=60)
		self.output_entry = tk.Entry (self.root, textvariable=self.default_output_str, width=60)
		self.username_entry = tk.Entry (self.root)
		self.race_entry = tk.Entry (self.root)



		self.browse_rep_button = tk.Button (self.root, text='Browse',command=self.browse_replay_dest, font=('Arial', 11, 'bold')) 
		self.browse_out_button = tk.Button (self.root, text='Browse',command=self.browse_output_filename, font=('Arial', 11, 'bold')) 
		self.done_button = tk.Button (self.root, text='Done',command=self.done, font=('Arial', 11, 'bold'))
		self.error_text = tk.Label(self.root, text="failed to install to directory", fg="red")

		self.complete = False
	
	def start(self):
		self.canvas.pack()
		self.canvas.create_window(400, 50, window=self.title)
		self.canvas.create_window(400, 150, window=self.dir_entry) 
		self.canvas.create_window(400, 250, window=self.output_entry) 
		self.canvas.create_window(400, 350, window=self.username_entry)
		self.canvas.create_window(400, 450, window=self.race_entry)

		self.canvas.create_window(400,100, window=self.rep_help)
		self.canvas.create_window(400,200, window=self.out_help)
		self.canvas.create_window(400,300, window=self.name_help)
		self.canvas.create_window(400,400, window=self.race_help)

		self.canvas.create_window(620, 150, window=self.browse_rep_button)
		self.canvas.create_window(620, 250, window=self.browse_out_button)

		self.canvas.create_window(400, 550, window=self.done_button)
		self.root.mainloop()

	def browse_replay_dest(self):
		dest = askdirectory()
		if dest != None and len(dest) > 0:
			self.default_replay_str.set(dest)
		return dest

	def browse_output_filename(self):
		fn = askopenfilename()
		if fn != None and len(fn) > 0:
			self.default_output_str.set(fn)
		return fn

	def done(self):
		err, err_str = self.validate_input()
		config_dict = {"scanDate":0.0, "replayPath":self.dir_entry.get(), "outputFile":self.output_entry.get(), "username":self.username_entry.get().lower().replace(" ", ""), "recordedRaces": self.race_entry.get().upper().replace(" ", "")}
		if (not err):
			SRS.update_config(config_dict, self.config_file)
			self.complete = True
			self.root.destroy()
		else:
			messagebox.showerror("Error", err_str)

	def validate_input(self):
		err = False
		err_str = ""

		replay_dir = self.dir_entry.get()
		if (not os.path.isdir(replay_dir)):
			err = True
			err_str += "Selected Replay Directory: {} does not exist\n".format(replay_dir)

		output_filename = self.output_entry.get()
		if (not output_filename.endswith(".csv")):
			err = True
			err_str += "Output file must end with .csv\n"

		usernames = self.username_entry.get()
		if (not len(usernames.split(",")) > 0 or len(usernames.split(",")[0]) < 1):
			err = True
			err_str += "Invalid username list\n"

		races = self.race_entry.get()
		accepted_races = ['Z', 'T', 'Z']
		r_in = races.upper().replace(" ", "").split(",")
		if len(r_in) < 1 or len(r_in[0]) < 1:
			err = True
			err_str += "Please Input a valid race (z,t,p)"
		else:
			for r in r_in:
				if r not in accepted_races:
					err = True
					err_str += "Invalid race {}".format(r)
		return err, err_str