import os
import shutil
import sys

class Application:
	BIN_PATH = r'C:\bin'
	_env_vars = []
	_exes = []

	def __init__(self, name, basedir):
		self.name = name
		self._basedir = basedir

	def addEnvironmentVariable(self, name, value):
		self._env_vars.append(name, value)

	def addExecutable(self, exe):
		self._exes.append(exe)

	def _rebase(self, val, new_basedir):
		if val.startswith(self._basedir):
			return val.replace(self._basedir, new_basedir)
		return val

	def changeBasedir(self, new_basedir):
		self._env_vars = [(key, _rebase(val, new_basedir)) for (key, val) in self._env_vars]
		self._basedir = new_basedir

	def createLaunchers(self, suffix=""):
		for exe in self.exes:
			launcher = open(os.path.join(BIN_PATH, exe.name + suffix + ".bat"), "w")
			launcher.write("@ECHO OFF\n")
			for key, val in self._env_vars:
				launcher.write("set ")
				launcher.write(key + "=\"" + val + "\"")
				launcher.write("\n")
			launcher.write("\n")
			if (launcher.gui):
				launcher.write("start \"\" ")
			launcher.write("\"" + os.path.join(self._basedir, exe.path) + "\"")
			launcher.write(" %*")
			launcher.write("\n")
			launcher.close()


class Executable:
	def __init__(self, name, path, gui=False):
		self.name = name
		self.path = path
		self.gui = gui


def MuxInstall(app, version):
	newbase = app.basedir + '-' + version
	shutil.copytree(app.basedir, newbase)
	app.changeBasedir(newbase)
	app.createLaunchers('-' + version)

def main():
	# IMPLEMENTATION MISSING!
	pass

if __name__=='__main__':
	main()
