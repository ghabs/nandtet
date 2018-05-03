// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// 0 will serve as flag for screen white (0) or screen black (1)
@0
M = 0
(LOOP)
// If KBD is !0 and M is 0, loop until black
@KBD
D = M
@0
D = D - M
@BLACKEN
D;JGT
// IF KBD is 0 and M is 0, loop until white
@WHITEN
D;JLT
// Repeat input check indefintely
@LOOP
0;JMP
(BLACKEN)
// Loop through all coordinates of screen and set pixel = 1
// i flag for loop
@1
M = 0
@0
M = 1
(LOOPSCREENB)
@1
D = M
@8000
D=D-A
@LOOP
D;JGT
// counter value
@1
D = M
@SCREEN
//Screen location to whiten/blacken
A=D+A
M = -1
@1
M = M + 1;
@LOOPSCREENB
0;JMP
// Loop through all coordinates of screen and set pixel = 1
(WHITEN)
// Loop through all coordinates of screen and set pixel = 1
// i flag for loop
@1
M = 0
@0
M = 0
(LOOPSCREENW)
@1
D = M
@8000
D=D-A
@LOOP
D;JGT
// counter value
@1
D = M
@SCREEN
//Screen location to whiten/blacken
A=D+A
M = 0
@1
M = M + 1;
@LOOPSCREENW
0;JMP
(END)
@END
0;JMP

