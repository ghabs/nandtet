// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

//Gets address of R2 and sets it to 0
@2
M=0
//Symbolic label marker to start the loop
(LOOP)
//Subtract one from R1
@0
D = M
D = D-1
M = D
@END
D;JLT //Jumps to end if R0 is < 0
//Sets D to the value in R2
@2
D = M
//Adds value in R1 to R2
@1
D = D + M
@2
M = D
@LOOP
0;JMP
(END)
@END
0;JMP

