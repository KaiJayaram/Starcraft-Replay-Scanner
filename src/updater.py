import git
import traceback
import os

def update():
	try:
		git_location = os.getcwd()
		repo = git.Repo(git_location)
		orig_hash = repo.head.object.hexsha
		g = git.cmd.Git(git_location)
		g.pull()
		new_hash = repo.head.object.hexsha
		return orig_hash != new_hash:

	except Exception:
		print("failed to reach git repo to pull updates")
		traceback.print_exc()

def main():
	update()

if __name__ == '__main__':
    main()
