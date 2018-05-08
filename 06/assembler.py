"""
Code for assembler, main routine.
CLI takes file as input, outputs binary.
"""

import regex
from patterns import *

class SymbolTable:
    def __init__(self):
        self.symbols = {}
        self.predefined_symbols = {
            "SP": "0",
            "LCL": "1",
            "ARG": "2",
            "THIS": "3",
            "THAT": "4",
            "R0": "0",
            "R1": "1",
            "R2": "2",
            "R3": "3",
            "R4": "4",
            "R5": "5",
            "R6": "6",
            "R7": "7",
            "R8": "8",
            "R9": "9",
            "R10": "10",
            "R11": "11",
            "R12": "12",
            "R13": "13",
            "R14": "14",
            "R15": "15",
            "SCREEN": "16384",
            "KBD": "24576"
        }
        # TODO: add st_counter sanity check
        self.st_counter = 16

    def lookup(self, symbol):
        return self.symbols[symbol]

    def load(self, field, nextline=0):
        """
        Only called on lines starting with @
        text: command[1..15]
        """
        if not self.predefined_symbols.get(field) and not self.symbols.get(field):
            if nextline:
                self.symbols[field] = nextline
                return
            self.symbols[field] = self.st_counter
            self.st_counter += 1
        return

    def run(self, text):
        """
        text: array of commands
        """
        #hacky way to account for moving the text for labels but shrug
        shift = 0
        for i,k in enumerate(text):
            if k[0] == "(":
                r = regex.sub("\(",'',k)
                r = regex.sub("\)",'',r)
                self.load(r,i-shift)
                shift += 1
        for k in text:
            if k[0] == "@" and not k[1:].isdigit():
                self.load(k[1:])
        
    def show_symbols(self):
        for k,v in self.symbols.items():
            print("{}:{}".format(k,v))

class Assembler:
    def __init__(self):
        self.symbols = {}
        self.predefined_symbols = {}
        self.compiled = []

    def parse(self, text):
        """Takes in a text file and splits it into fields that can be tokenized"""
        array = []
        with open(text, 'r') as f:
            for line in f:
                if line[0] != "/":
                    l = line.rstrip().strip()
                    if l != '':
                        array.append(l)
        return array

    def manipulate_dest(self, dest_text):
        return symbols[dest_text]

    def manipulate_jmp(self, jmp_text):
        return symbols[jmp_text]

    def manipulate_command(self, cmd_text):
        return commands[cmd_text]

    def make_c_inst(self, cmd):
        "todo: stop copying string and modify in place"
        inst = c_inst
        l = cmd.replace('=',' ').split()
        if not len(l) > 1:
            inst = inst.replace('d','0')
        else: 
            inst = inst.replace('ddd', self.manipulate_dest(l.pop(0))) 
        l = l.pop().replace(';',' ').split()
        if not len(l) > 1:
            inst = inst.replace('j','0')
        else:
            inst = inst.replace('jjj', self.manipulate_jmp(l.pop()))
        inst = inst.replace('acccccc', self.manipulate_command(l[0]))
        return inst

    def translate(self,text):
        symbols = {**self.symbols, **self.predefined_symbols}
        for i in text:
            if i[0] == "(":
                pass
            elif i[0] == "@":
                inst = a_inst
                cmd = symbols.get(i[1:])
                if not cmd:
                    self.compiled.append(inst.replace('bbbbbbbbbbbbbbb', format(int(i[1:]), '015b')))
                else:
                    self.compiled.append(inst.replace('bbbbbbbbbbbbbbb', format(int(cmd), '015b')))
            else:
                self.compiled.append(self.make_c_inst(i))

    def write_out(self, file):
        with open(file, 'w') as f:
            for i in self.compiled:
                f.write(i+"\n")
    
    def load_symbols(self,symbols,pd):
        self.symbols=symbols
        self.predefined_symbols = pd

def main():
    assembler = Assembler()
    text = assembler.parse("pong/Pong.asm")
    st = SymbolTable()
    st.run(text)
    st.show_symbols()
    assembler.load_symbols(st.symbols, st.predefined_symbols)
    assembler.translate(text)
    assembler.write_out("output.hack")



if __name__ == "__main__":
    main()

