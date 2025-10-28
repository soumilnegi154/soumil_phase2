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

# 2. Armssembly 1   

> For what argument does this program print `win` with variables 83, 0 and 3? File: [chall_1.S](resources/reverse-engineering/armssembly/chall_1.S) Flag format: picoCTF{XXXXXXXX} -> (hex, lowercase, no 0x, and 32 bits. ex. 5614267 would be picoCTF{0055aabb})

## Solution:

First we read the file using `cat`
```sh
┌──(kali㉿kali)-[~/Desktop/picoCTF/armssembly1]
└─$ cat chall_1.S 
        .arch armv8-a
        .file   "chall_1.c"
        .text
        .align  2
        .global func
        .type   func, %function
func:
        sub     sp, sp, #32
        str     w0, [sp, 12]
        mov     w0, 83
        str     w0, [sp, 16]
        str     wzr, [sp, 20]
        mov     w0, 3
        str     w0, [sp, 24]
        ldr     w0, [sp, 20]
        ldr     w1, [sp, 16]
        lsl     w0, w1, w0
        str     w0, [sp, 28]
        ldr     w1, [sp, 28]
        ldr     w0, [sp, 24]
        sdiv    w0, w1, w0
        str     w0, [sp, 28]
        ldr     w1, [sp, 28]
        ldr     w0, [sp, 12]
        sub     w0, w1, w0
        str     w0, [sp, 28]
        ldr     w0, [sp, 28]
        add     sp, sp, 32
        ret
        .size   func, .-func
        .section        .rodata
        .align  3
.LC0:
        .string "You win!"
        .align  3
.LC1:
        .string "You Lose :("
        .text
        .align  2
        .global main
        .type   main, %function
main:
        stp     x29, x30, [sp, -48]!
        add     x29, sp, 0
        str     w0, [x29, 28]
        str     x1, [x29, 16]
        ldr     x0, [x29, 16]
        add     x0, x0, 8
        ldr     x0, [x0]
        bl      atoi
        str     w0, [x29, 44]
        ldr     w0, [x29, 44]
        bl      func
        cmp     w0, 0
        bne     .L4
        adrp    x0, .LC0
        add     x0, x0, :lo12:.LC0
        bl      puts
        b       .L6
.L4:
        adrp    x0, .LC1
        add     x0, x0, :lo12:.LC1
        bl      puts
.L6:
        nop
        ldp     x29, x30, [sp], 48
        ret
        .size   main, .-main
        .ident  "GCC: (Ubuntu/Linaro 7.5.0-3ubuntu1~18.04) 7.5.0"
        .section        .note.GNU-stack,"",@progbits
```
Here we can see `main` function is calling `func` and in `func` - 
```sh
func:
        sub     sp, sp, #32                 #allocates 32bit to stack
        str     w0, [sp, 12]                #puts w0 at [sp, 12]
        mov     w0, 83                      #w0=83
        str     w0, [sp, 16]                #w0 at [sp,16]
        str     wzr, [sp, 20]               #puts wzr at [sp, 20], wzr=0
        mov     w0, 3                       #w0=3 at [sp, 16]
        str     w0, [sp, 24]                #w0=3 at [sp, 24]
        ldr     w0, [sp, 20]                #loads [sp, 20] to w0 ie: w0=0
        ldr     w1, [sp, 16]                #loads [sp, 16] to w1, ie: w1=83
        lsl     w0, w1, w0                  #logical shift left to w1 by w0, ie: w0 = 83 << 0 = 83
        str     w0, [sp, 28]                #w0 = 83 at [sp, 28]
        ldr     w1, [sp, 28]                #w1 = 83
        ldr     w0, [sp, 24]                #w0 = 3
        sdiv    w0, w1, w0                  #w0 = 83/3 = 27
        str     w0, [sp, 28]                #w0 = 27 at [sp, 28]
        ldr     w1, [sp, 28]                #w1 = 27
        ldr     w0, [sp, 12]                #w0 = input from user
        sub     w0, w1, w0                  #w0 = w1-w0
        str     w0, [sp, 28]                #w0 = 27-w0 at [sp, 28]
        ldr     w0, [sp, 28]                 
        add     sp, sp, 32
        ret
        .size   func, .-func
        .section        .rodata
        .align  3
```

Thus for win condition, LC0 should be 0 ie: 27-w0 = 0, thus w0 = 27, and 27 in hex is `001B`.


## Flag:

```
picoCTF{0000001b}
```

## Concepts learnt:

- Assembly

## Resources:

- [https://www.youtube.com/watch?v=6S5KRJv-7RU&t=75s](https://www.youtube.com/watch?v=6S5KRJv-7RU&t=75s)
- [https://www.youtube.com/watch?v=BUlPvdz8z-I](https://www.youtube.com/watch?v=BUlPvdz8z-I)


***

# 3. Vault Door 3

> This vault uses for-loops and byte arrays. The source code for this vault is here: [VaultDoor3.java](resources/reverse-engineering/vaultdoor3/VaultDoor3.java)

## Solution:

The file contains the code
```sh
┌──(kali㉿kali)-[~/Desktop/picoCTF/vaultdoor3]
└─$ cat VaultDoor3.java 
import java.util.*;

class VaultDoor3 {
    public static void main(String args[]) {
        VaultDoor3 vaultDoor = new VaultDoor3();
        Scanner scanner = new Scanner(System.in);
        System.out.print("Enter vault password: ");
        String userInput = scanner.next();
        String input = userInput.substring("picoCTF{".length(),userInput.length()-1);
        if (vaultDoor.checkPassword(input)) {
            System.out.println("Access granted.");
        } else {
            System.out.println("Access denied!");
        }
    }

    // Our security monitoring team has noticed some intrusions on some of the
    // less secure doors. Dr. Evil has asked me specifically to build a stronger
    // vault door to protect his Doomsday plans. I just *know* this door will
    // keep all of those nosy agents out of our business. Mwa ha!
    //
    // -Minion #2671
    public boolean checkPassword(String password) {
        if (password.length() != 32) {
            return false;
        }
        char[] buffer = new char[32];
        int i;
        for (i=0; i<8; i++) {
            buffer[i] = password.charAt(i);
        }
        for (; i<16; i++) {
            buffer[i] = password.charAt(23-i);
        }
        for (; i<32; i+=2) {
            buffer[i] = password.charAt(46-i);
        }
        for (i=31; i>=17; i-=2) {
            buffer[i] = password.charAt(i);
        }
        String s = new String(buffer);
        return s.equals("jU5t_a_sna_3lpm18g947_u_4_m9r54f");
    }
}
```

This can be reverse engineered using the script

```python
password = "jU5t_a_sna_3lpm18g947_u_4_m9r54f"
trial = []
for i in range(32):
    trial.append(" ")
for i in range(0,8,1):
    trial[i] = password[i]
for i in range(8,16,1):
    trial[i] = password[23-i]
for i in range(16, 32, 2):
    trial[i] = password[46-i]
for i in range(31, 16, -2):
    trial[i] = password[i]
    
for i in range(len(trial)):
    print(trial[i], end="")
```


## Flag:

```
picoCTF{jU5t_a_s1mpl3_an4gr4m_4_u_79958f}
```

## Concepts learnt:

- JAVA syntax

***