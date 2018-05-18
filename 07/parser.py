from vm_defs import Command

class Parser:
    def __init__(self, f):
        self.current_cmd = []
        self.file_loc = f
    
    def commandType(self, c):
        """
        Return C_ARITHMETIC, C_PUSH, C_POP, C_LABEL,
        C_GOTO, C_IF, C_FUNCTION, C_RETURN, C_CALL
        """
        c = c.lower()
        if c == "add" or c == "sub" or c == "neg" or c == "eq" or c == "not" or c == "gt" or c == "lt" or c == "or" or c == "and":
            return "C_ARITHMETIC"
        if c == "push":
            return "C_PUSH"
        if c == "pop":
            return "C_POP"
        if c == "label":
            return "C_LABEL"
        if c == "goto":
            return "C_GOTO"
        if c == "if-goto":
            return "C_IF"
        if c == "function":
            return "C_FUNCTION"
        if c == "call":
            return "C_CALL"
        if c == "return":
            return "C_RETURN"
    
    def arg1(self, c):
        """Return the first argument"""
        return c.upper()
    
    def arg2(self, c):
        """Return the second argument"""
        return str(c).upper()
    
    def parse(self):
        instructions = []
        with open(self.file_loc, 'r') as f:
            for line in f:
                "Clean the line and check number of arguments"
                if line[0] == "/" or line == '':
                    continue                 
                self.current_cmd = line.strip().split()
                l = len(self.current_cmd)
                if l == 0:
                    continue
                ct = self.commandType(self.current_cmd[0])
                if ct == "C_ARITHMETIC":
                    a1 = self.current_cmd[0].upper()
                elif l > 1:
                    a1 = self.arg1(self.current_cmd[1])
                if l > 2:
                    a2 = self.arg2(self.current_cmd[2])
                instructions.append(Command(ct,a1,a2))
                #TODO: write as yield, generator
        return instructions
