#coding = utf-8

import sys
from File import File
from Execute import Execute

def test():
	isKeep = True
	dstFileName = None
	
	argsLen = len(sys.argv)
	if argsLen < 2:
		sys.exit()
	
	if argsLen >= 3:
		if sys.argv[2].startswith('-nk'):
			isKeep = False
		if argsLen > 3:
			dstFileName = sys.argv[3]
		
	srcFile = File(sys.argv[1], isKeep, dstFileName) 
	srcFile.parse()

	exe = Execute(srcFile.dstFileName)
	exe.run()

if __name__ == '__main__':
	test()
