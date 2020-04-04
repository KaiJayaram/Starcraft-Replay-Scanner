import starcraft_replay_scanner as SRS 
import starcraft_replay_scanner_gui as SRSGUI 
from setup_gui import Setup_GUI
import os.path
import time
from updater import update
from tkinter import messagebox

class SRSOrchestrator():
	def __init__(self):
		self.run_delay = 30
		self.config_file = "starcraft_replay_scanner.config"
	def run(self):
		if (update()):
			messagebox.showinfo("Update Available", "Update Available Please Restart program")

		if not os.path.exists(self.config_file):
			setup_gui = Setup_GUI(self.config_file)
			setup_gui.start()
			while(not setup_gui.complete):
				time.sleep(1)
		srs_gui = SRSGUI.Run_GUI(self, self.run_delay)
		srs_gui.start()


def main():
	orchestrator = SRSOrchestrator()
	orchestrator.run()

if __name__ == '__main__':
	main()