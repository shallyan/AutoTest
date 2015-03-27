#coding = utf-8

FUNCTION = '//FUNC'

IN = '//IN'

RET = '//RET'

TEST_CODE_RET = 'void'

TEST_CODE_PREFIX = 'test_'

VARIABLE_RE = '[_a-zA-Z][_a-zA-Z0-9]*'

COMPILING_FILE_PREFIX = 'test_'

COMPILING_FILE_HEADER = '#include <stdio.h>\n#include <stdlib.h>\n'

COMPILING_FILE_DRIVER_PREFIX = '\nint\nmain()\n{\n'

COMPILING_FILE_DRIVER_POSTFIX = '\treturn 0;\n}'
