import git
import traceback
import os

def update():
	try:
		cwd = os.getcwd()
		# go up one directory
		git_location = os.path.dirname(cwd)

		g = git.cmd.Git(git_location)
		g.pull()
	except Exception:
		print("failed to reach git repo to pull updates")
		traceback.print_exc()

def main():
	update()

if __name__ == '__main__':
    main()
