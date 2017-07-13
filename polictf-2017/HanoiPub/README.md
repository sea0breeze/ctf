# HanoiPub Writeup
Some Googling tells us that this file is Intel HEX format. Convert it to binary format by objcopy and we can load it by IDA. As its architectrue is AVR, its code address space and its data address space is separated and its way to load/store data is so strange. So it seems that IDA can't deal with it properly(But I think it's at least better than using objdump).

After hours of reading documentation of avr and analyzing the program, I got the following deduction: (The address showed in IDA is different from raw file)

*	sub_87 is used to print bytes, given str pointer and length;
* 	sub_4c5 is "printf"
*  	sub_2e9 is "main"
*	the data section is loaded by lpm instructions in _RESET
* 	the strings about "%d bottles of beer" have nothing to do with the flag
*  	The fun part is around 0x425-0x426 ---- the eor instructions

In fact, there is an int16 array ended with 0x1(not included). For each word, it tries to minus it with index+1 and ++tmp(init as 1) again and again, until the word is decreased to 0(namely, tmp = array[i] / (i+1)). Then tmp -= 0x30, and xor it with the corresponding byte in "To beer or not to beer, that is the question". I try to find out the result and it appears to be flag :) 