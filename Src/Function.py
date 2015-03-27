#oding = utf-8

try:
	import cStringIO as StringIO
except ImportError:
	import StringIO

import Config
import re

class InRetTestCase(object):
	def __init__(self, funcIn, funcComp):
		self.funcIn = funcIn
		self.funcComp = funcComp

class Function(object):
	def __init__(self, funcText):
		self.name = "<unknown>"
		self.textFile = StringIO.StringIO(funcText)
		self.retType = "<unknown>"
		self.argsType = []
		self.testFuncName = "<unknown>"
		self.testCode = ""
		self.testCases = []
		self.caseCount = 0
	
	def __enter__(self):
		return self
	
	def __exit__(self, exc_type, exc_value, traceback):
		self.close()
		if exc_type != None:
			raise Exception('Function exit exception: ' + str(traceback) )

	def __readLine(self):
		return self.textFile.readline().strip()
	
	def __parseReturnType(self, retTypeStr):
		self.retType=retTypeStr

	def __parsePrototype(self, prototypeStr):
		#function name
		lBracket = prototypeStr.find('(')
		if lBracket == -1:
			raise Exception('Invalid function prototype: missing {\n')
		
		funcName = prototypeStr[0 : lBracket]
		self.name = funcName.strip()

		#args type
		rBracket = prototypeStr.find(')')
		if rBracket == -1:
			raise Exception('Invalid function prototype: missing }\n')

		args = prototypeStr[lBracket+1 : rBracket].split(',')
		for i in range(len(args)):
			variables = re.findall(Config.VARIABLE_RE, args[i])
			if len(variables) == 0:
				raise Exception('Invalid function arguments')
				
			lIndex = args[i].rfind(variables[-1])
			if lIndex != -1:
				args[i] = args[i][0 : lIndex]
		self.argsType = args

	def __generateTestCodePrefix(self):
		self.testCode = Config.TEST_CODE_RET + '\n' + Config.TEST_CODE_PREFIX
		#function name
		self.testCode += self.name + '()'
		self.testFuncName = Config.TEST_CODE_PREFIX + self.name 
		#function body
		self.testCode += '\n{\n'
	
	def __generateTestCodePostfix(self):
		self.testCode += '}\n'

	def __parserVariableName(self,codeStr):
		return re.findall(Config.VARIABLE_RE,codeStr)		
	
	def __convertVariableName(self,codeStr):
		variables = re.findall(Config.VARIABLE_RE, codeStr);
		for i in range(len(variables)):
			var = self.argsType[i] + variables[i] + str(self.caseCount)
			codeStr = re.sub(variables[i], var, codeStr, 1)
		
		return re.sub(';[ ]*', ';\n\t',codeStr)
	
	def __generateInRetCase(self, funcIn, funcRet):
		pFuncIn = '\t' + self.__convertVariableName(funcIn) + '\n'
		pFuncComp = '\t' + 'if(' + funcRet + ' != ' +self.name + '('
		#function arguments
		args = self.__parserVariableName(funcIn)
		
		for arg in args:
			pFuncComp += arg + str(self.caseCount) + ', '
		pFuncComp = pFuncComp[0 : -2]

		pFuncComp += ') )\n\t{\n\t\tprintf("'+ self.name + ': Case ' + str(self.caseCount) + ' fail.\\n");'
		pFuncComp += '\n\t\texit(1);\n\t}\n\n'

		self.testCases.append(InRetTestCase(pFuncIn, pFuncComp) )
		self.caseCount += 1

	def __generateTestCodeBody(self):	
		for case in self.testCases:
			self.testCode += case.funcIn
		
		for case in self.testCases:
			self.testCode += case.funcComp

	def parse(self):
		#returned type
		retTypeStr = self.__readLine()
		self.__parseReturnType(retTypeStr)
		
		#function prototype
		prototypeStr = self.__readLine()
		self.__parsePrototype(prototypeStr)
		
		#testing data
		self.__generateTestCodePrefix()
		
		while True:
			dataStr = self.__readLine()
			if dataStr.startswith(Config.IN):
				#start one case
				funcIn = self.__readLine()
				while not self.__readLine().startswith(Config.RET): 
					self.__readLine()
				funcRet=self.__readLine()

				self.__generateInRetCase(funcIn, funcRet)
			elif dataStr.startswith('*/'):
				break;
		
		self.__generateTestCodeBody()
		self.__generateTestCodePostfix()

	def close(self):
		self.textFile.close()
