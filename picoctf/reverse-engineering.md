# 1. GDB baby step 1

> Can you figure out what is in the eax register at the end of the main function? Put your answer in the picoCTF flag format:  picoCTF{n} where n is the contents of the eax register in the decimal number base. If the answer was 0x11 your flag would be  picoCTF{17}. Disassemble [this](resources/reverse-engineering/gdb/debugger0_a).

## Solution:

Since the hint recommends us GDB disassembler, we need to open the file in gdb and disassemble the `main` function,
```sh
┌──(kali㉿kali)-[~/Desktop/picoCTF/gdb babystep1]
└─$ gdb debugger0_a 
GNU gdb (Debian 16.3-5) 16.3
Copyright (C) 2024 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
Type "show copying" and "show warranty" for details.
This GDB was configured as "x86_64-linux-gnu".
Type "show configuration" for configuration details.
For bug reporting instructions, please see:
<https://www.gnu.org/software/gdb/bugs/>.
Find the GDB manual and other documentation resources online at:
    <http://www.gnu.org/software/gdb/documentation/>.

For help, type "help".
Type "apropos word" to search for commands related to "word"...
Reading symbols from debugger0_a...
(No debugging symbols found in debugger0_a)
(gdb) disassemble main
Dump of assembler code for function main:
   0x0000000000001129 <+0>:     endbr64
   0x000000000000112d <+4>:     push   %rbp
   0x000000000000112e <+5>:     mov    %rsp,%rbp
   0x0000000000001131 <+8>:     mov    %edi,-0x4(%rbp)
   0x0000000000001134 <+11>:    mov    %rsi,-0x10(%rbp)
   0x0000000000001138 <+15>:    mov    $0x86342,%eax
   0x000000000000113d <+20>:    pop    %rbp
   0x000000000000113e <+21>:    ret
End of assembler dump.
```
Here since the output is being sent to eax at address 0x86342, we can read the output using print,

```sh
(gdb) print 0x86342
$1 = 549698
```

## Flag:

```
picoCTF{549698}
```

## Concepts learnt:

- GNU Project Debugger

## Notes:

- Include any alternate tangents you went on while solving the challenge, including mistakes & other solutions you found.
- We can print variable values using `print`, disassemble functions using `disassemble` and view functions using `info functions`.

## Resources:

- [https://www.geeksforgeeks.org/c/gdb-step-by-step-introduction/](https://www.geeksforgeeks.org/c/gdb-step-by-step-introduction/)

***

# 2. Challenge name

> Description

.
.
.
