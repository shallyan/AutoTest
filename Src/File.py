#coding = utf-8

import os
import Config
from Function import Function


class File(object):
	def __init__(self, srcFileName, isKeep = False, dstFileName = None):
		self.srcFileName = srcFileName
		self.isKeep = isKeep
		self.dstFileName = dstFileName
		self.testFuncs = [] 
		self.codeLines = None
		
		self.__readCode()

	def __readCode(self):
		if not os.path.exists(self.srcFileName):
			raise Exception('Invalid file paht\n')
		
		with open(self.srcFileName, 'r') as f:
			self.codeLines = f.readlines()
	
	def __generateSourceCode(self):
		if not self.isKeep:
			os.remove(self.srcFileName)
			self.dstFileName = self.srcFileName
		elif self.dstFileName == None:
			self.dstFileName = Config.COMPILING_FILE_PREFIX + self.srcFileName

		with open(self.dstFileName, 'w') as f:
			#header and function 
			codeStr = Config.COMPILING_FILE_HEADER + '\n' + ''.join(self.codeLines)
			#test code
			for testFunc in self.testFuncs:
				codeStr += '\n' + testFunc[1]
			#driver
			codeStr += Config.COMPILING_FILE_DRIVER_PREFIX
			for testFunc in self.testFuncs:
		  		codeStr += '\t' + testFunc[0] + '();\n\n'
			codeStr += Config.COMPILING_FILE_DRIVER_POSTFIX
			f.write(codeStr)

	def parse(self):
		isFunc = False
		funcStr = ""

		for line in self.codeLines:
			if(line.strip().startswith(Config.FUNCTION) ):
				#begin one function
				isFunc = True
				funcStr = ""
			elif isFunc:
				funcStr += line
				if line.strip().startswith('*/'):
					isFunc = False
					with Function(funcStr) as func:
						func.parse()
						self.testFuncs.append( (func.testFuncName, func.testCode) )

		self.__generateSourceCode()
