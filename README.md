# AutoTest

##Introduction
This simple tool can be used for generating testing part for C functions, which means you can just write the function and the testing cases. I spent one day to create this simple version 1.0 because I am practising algorithms recently, and writing testing code is so boring and repetitive, and I hope it will be also convenient for you if you would like to have a try.

##Usage
Up to now, one line "//FUNC" must be right before the C function to indicate the tested function, and the "//IN" to indicate the input of the function, which can't be more than one line and we use "//RET" to indicate the return value.The C function must be standard format, which means the return type in a separate line. 

All the symbols are listed below:
* //FUNC: the start of a function 
* //IN: one input case
* //RET: one return value

For example:
```c
//FUNC
int
sum(int A[], int N)
{
	/*
		//IN
		A[3] = {1, 2, 3}; N = 3;
		//RET
		6
		//IN
		A[2] = {1, 2}; N = 2;
		//RET
		3
	*/
	int i, total = 0;
	
	for(i = 0; i < N; i++)
		total += A[i];
	
	return total;
}
```

Notes 
* Type. The input needs to be written like C code, but don't need to add the data type, which will be added automatically.
* Name. The name of the variables can be arbitrary and it's ok be the same in different test cases, which will be renamed automatically.
* Order. The order of the input must be the same with the arguments declared in the function prototype.
* Indicator. The "//FUNC" is not necessary for every function and you just need add this label for the function you want to test.Even if you add the "//FUNC", but you don't write the test cases, the test code of this function will not be generated.

##Commands
Under the Linux with Python, if you have a source file named *file.c* ,you could use this tool by typing this command:
```shell
python Tester.py file.c
```
Then a new file called test_file.c will be created, which contains the function and the test code.

If you don't want to create a new file, you can use the below command:
```shell
python Tester.py file.c -nk
```
Then the file.c will contains the testCode.

By default, the new test file is just add a prefix "test_" before your file. So if you want to rename this file, you can add one more argument:
```c
python Tester.py file.c dd newfile.c
```
Noted that if you rename the file containing the test code, the third argument which indicates whether to keep original file can be arbitrary.

No matter whether we generate a new file, the source file containing test code will then be executed by gcc, thus checking all the test and showing the result.

##Examples
If we have a C source file *sum.c*
```c
//FUNC
int
sum(int A[], int N)
{
	/*
		//IN
		A[3] = {1, 2, 3}; N = 3;
		//RET
		6
		//IN
		A[2] = {1, 2}; N = 2;
		//RET
		3
	*/
	int i, total = 0;
	
	for(i = 0; i < N; i++)
		total += A[i];
	
	return total;
}
```
Then this tool will generate test file like below:
```c
#include <stdio.h>
#include <stdlib.h>

//FUNC
int
sum(int A[], int N)
{
	/*
		//IN
		A[3] = {1, 2, 3}; N = 3;
		//RET
		6
		//IN
		A[2] = {1, 2}; N = 2;
		//RET
		3
	*/
	int i, total = 0;
	
	for(i = 0; i < N; i++)
		total += A[i];
	
	return total;
}

void
test_sum()
{
	int A0[3] = {1, 2, 3};
	int N0 = 3;
	
	int A1[2] = {1, 2};
	int N1 = 2;
	
	if(6 != sum(A0, N0) )
	{
		printf("sum: Case 0 fail.\n");
		exit(1);
	}

	if(3 != sum(A1, N1) )
	{
		printf("sum: Case 1 fail.\n");
		exit(1);
	}

}

int
main()
{
	test_sum();

	return 0;
}
```

The output is shown below:
```c
gcc compiles successfully.
test_sum runs successfully, and pass all the tests.
```

If we modify the second test case to make it wrong, the output will be like this (Noted that the index starts from zero):
```c
gcc compiles successfully.
sum: Case 1 fail.
[Error]: test_sum can not pass all the tests.
```