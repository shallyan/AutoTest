#coding = utf-8

import subprocess

class Execute(object):
	def __init__(self, fileName):
		self.fileName = fileName
		self.exeName = None

		self.compile()

	def compile(self):
		dotIndex = self.fileName.find('.')
		exeName = self.fileName[0 : dotIndex]
		if dotIndex == -1:
			exeName += self.fileName[-1]
	
		cmd = 'gcc ' + self.fileName + ' -o ' + exeName 
		retCode = subprocess.call(cmd, shell = True)

		if retCode:
			print '[Error]: there is something wrong when compiling with gcc.'
		else:
			print 'gcc compiles successfully.'
			self.exeName = exeName
	
	def run(self):
		if self.exeName != None:
			cmd = './' + self.exeName
			retCode = subprocess.call(cmd, shell = True)

			if retCode:
				print '[Error]: ' + self.exeName + ' can not pass all the tests.'
			else:
				print self.exeName + ' runs successfully, and pass all the tests.'
