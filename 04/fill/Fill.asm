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

@BLCOUNT
M=0
@WHCOUNT
M=0
(INPUT)
	@KBD
	D=M
	@BLACKEN
	D;JNE
	@WHITEN
	D;JEQ
(BLACKEN)
	@WHCOUNT
	M=0
	@BLCOUNT
	D=M
	@8192
	D=D-A
	@INPUT
	D;JEQ

	@BLCOUNT
	D=M
	M=M+1

	@SCREEN
	A=A+D
	M=-1
	@INPUT
	0;JEQ
(WHITEN)
	@BLCOUNT
	M=0
	@WHCOUNT
	D=M
	@8192
	D=D-A
	@INPUT
	D;JEQ

	@WHCOUNT
	D=M
	M=M+1

	@SCREEN
	A=A+D
	M=0
	@INPUT
	0;JEQ
