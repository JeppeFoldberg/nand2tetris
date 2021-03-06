#!/usr/bin/python
import sys

"""
Dette script er lavet til et af mine hobby-projekter; nand2tetris. Det er et kursus der er lavet for at give et simpelt overblik
af hvordan en computer er bygget fra bunden og op. Her har jeg lavet en assembler der tager imod simpel assemblykode og omdanner det
til binær maskinkode som den simple computer jeg har bygget (virtuelt) kan forstå. Når jeg nu skal vise dette script bliver jeg konfronteret
med hvor dårlig jeg har været til at skrive kommentarer til den. Jeg er meget opmærksom på at ordentlige kommentarer er med til at gøre 
ens kode forståeligt for andre men eftersom jeg kun har skrevet dette script for min egen skyld har jeg været lidt for afslappet omkring det.

Helt grundlæggende tager den imod en tekstfil og outputter en .hack fil (filformatet til førnævnte computer!). Først gennemgår den tekstfilen 
for symboler der endnu ikke er i symbol-ordbogen.Hvis de ikke er i symbol-ordbogen bliver de tilføjet og får en ubrugt adresse i hack-computerens
hukommelse. Derefter gennemgår den scriptet og omdanner hver linje til en binær kode primært ved at matche linjens indhold med de forskellige ord-
bøger der indeholder de rigtige binære koder! 

I projektet nand2tetris foreskriver de egentlig en anden (mere kompliceret) måde at bygge assembleren på. Her har jeg taget en genvej ved at udnytte
pythons måde at fungere på. Får jeg ekstra tid en dag kunne jeg godt tænke mig at bygge assembleren efter deres specifikationer, for at få et bredere
perspektiv på forskellige programmerings-praksisser og -sprog.
"""

script, assemblycode = sys.argv
filename = assemblycode.split(".")[0] + ".hack"

compdict = {"0": "0101010", "1": "0111111", "-1": "0111010", "D": "0001100", "A": "0110000",
            "!D": "0001101", "!A": "0110001", "-D": "0001111", "-A": "0110011", "D+1": "0011111",
            "A+1": "0110111", "D-1": "0001110", "A-1": "0110010", "D+A": "0000010", "D-A": "0010011",
            "A-D": "0000111", "D&A":"0000000", "D|A": "0010101", "M":"1110000", "!M": "1110001",
            "-M": "1110011", "M+1": "1110111", "M-1": "1110010", "D+M": "1000010", "D-M": "1010011",
            "M-D": "1000111", "D&M": "1000000", "D|M": "1010101"}
destdict = {"M": "001", "D": "010", "MD": "011", "A": "100", "AM": "101", "AD": "110", "AMD": "111"}
jumpdict = {"JGT": "001", "JEQ": "010", "JGE": "011", "JLT": "100", "JNE": "101", "JLE": "110", "JMP": "111"}
symboldict = {"SP": "0000000000000000", "LCL": "0000000000000001", "ARG": "0000000000000010",
              "THIS": "0000000000000011", "THAT": "0000000000000100", "R0": "0000000000000000",
              "R1": "0000000000000001", "R2": "0000000000000010", "R3": "0000000000000011",
              "R4": "0000000000000100", "R5": "0000000000000101", "R6": "0000000000000110",
              "R7": "0000000000000111", "R8": "0000000000001000", "R9": "0000000000001001",
              "R10": "0000000000001010", "R11": "0000000000001011", "R12": "0000000000001100",
              "R13": "0000000000001101", "R14": "0000000000001110", "R15": "0000000000001111",
              "SCREEN": "0100000000000000", "KBD": "0110000000000000"}


with open(assemblycode, "r") as f:
    romcounter = 0
    for line in f:  # TODO check that this parser actually works!
        line = line.strip()
        line = line.rstrip("\r\n")
        if len(line) < 1:
            continue
        if line[0:2] == "//":
            continue
        if "//" in line:
            line = line.split("//")[0].rstrip()
        first = line[0]
        if first == "@" or first == "D" or first == "M" or first == "A" or first == "0":
            romcounter += 1
        if line[0] == "(":
            symboldict[line.strip("()")] = "{:016b}".format(romcounter)


with open(assemblycode, "r") as f, open(filename, "w") as f2:
    counter = 16
    for line in f:
        line = line.strip()
        line = line.rsplit("//")[0]
        line = line.rstrip("\r\n")
        if len(line) < 1:
            continue
        if line[0:2] != "//":
            if "//" in line:
                line = line.split("//")[0].rstrip("\r\n ")
        if line[0] == "/":
            continue
        elif line[0] == "\r":
            continue
        elif "@" in line:
            line = (line.split("//")[0].rstrip())
            line = line.strip("@")
            if line[0].isdigit():
                f2.write("0" + "{:015b}".format(int(line)) + "\r\n")
            else:
                try:
                    f2.write(symboldict[line] + "\r\n")
                except KeyError:
                    number = "0" + "{:015b}".format(counter)
                    symboldict[line] = number
                    counter += 1
                    f2.write(symboldict[line] + "\r\n")
        elif "(" in line:
            continue
        else:
            line = str(line.split("//")[0].rstrip("\r\n"))
            line = line.strip()
            if ";" in line:
                jump = jumpdict[line[-3:]]
                line = line[:-4]
            else:
                jump = "000"
            if "=" in line:
                destination = line.split("=")[0]
                dest = destdict[str(destination)]
                line = line.split("=")[1]
            else:
                dest = "000"
            compbin = compdict[line]
            f2.write("111" + compbin + dest + jump + "\r\n")