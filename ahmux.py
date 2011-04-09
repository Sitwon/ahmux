import ConfigParser
import os
import shutil
import sys

DEBUG = True

def debug(msg):
	if DEBUG:
		print msg


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
			debug("Creating launcher: " + launcher)
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
	debug("Copying install to: " + newbase)
	shutil.copytree(app.basedir, newbase)
	debug("Rebasing the app.")
	app.changeBasedir(newbase)
	debug("Creating launchers.")
	app.createLaunchers('-' + version)

def main():
	# IMPLEMENTATION MISSING!
	debug("Reading config file: " + sys.argv[1])
	config = ConfigParser.RawConfigParser()
	config.readfp(open(sys.argv[1], 'r'))
	debug("Creating app: " + config.get('application', 'name'))
	debug("With basepath: " + config.get('application', 'basepath'))
	app = Application(config.get('application', 'name'), config.get('application', 'basepath'))
	for name, value in config.items('environment'):
		debug("Adding EV: " + name + "=" + value)
		app.addEnvironmentVariable(name, value)
	for name in config.get('application', 'exes').split(','):
		name = name.strip()
		debug("Adding exe: " + name)
		debug("With path: " + config.get(name, 'path'))
		debug("GUI: " + config.get(name, 'gui'))
		app.addExecutable(Executable(name, config.get(name, 'path'), config.getboolean(name, 'gui')))
	debug("MuxInstalling as version: " + config.get('application', 'version'))
	MuxInstall(app, config.get('application', 'version'))
	debug("Done.")

if __name__=='__main__':
	main()
