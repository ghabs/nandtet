from vm_defs import Command

class Writer:
    def __init__(self, file_loc):
        self.f = file_loc
        self.sp = 256
        self.label = 0
        self.lcl = 2048
        self.arg = 2056
        self.pointer = 2064
        self.thatOffset = 8
        self.temp = 5
        self.static = 16
        self.funcName = "sys"
    
    #todo remove/rename
    def changeSP(self, i):
        self.sp += i
        return self.updateSP()
    
    def updateSP(self):
        return "@{}\nD=A\n@0\nM=D\n".format(self.sp)

    def writeArithmetic(self, cmd):
        """Write out arithmetic function to file"""
        s = ""
        if cmd.ct == "C_ARITHMETIC":
            if cmd.a1 == "ADD":
                self.sp += -1
                s += "@{}\n".format(self.sp)
                s += "D=M\n"
                self.sp += -1
                s += "@{}\n".format(self.sp)
                s += "M=D+M\n"
            if cmd.a1 == "SUB":
                self.sp += -1
                s += "@{}\n".format(self.sp)
                s += "D=M\n"
                self.sp += -1
                s += "@{}\n".format(self.sp)
                s += "M=D-M\n"
            if cmd.a1 == "NEG":
                self.sp += -1
                s += "@{}\n".format(self.sp)
                s += "M=-M\n"
            if cmd.a1 == "NOT":
                self.sp += -1
                s += "@{}\n".format(self.sp)
                s += "M=!M\n"
            if cmd.a1 == "EQ":
                self.sp += -1
                s += "@{}\n".format(self.sp)
                s += "D=M\n"
                self.sp += -1
                s += "@{}\n".format(self.sp)
                s += "D=D-M\n"
                #Jump function that sets x == 1 if x&y are eq
                #Rewrite to be function
                s += "@eq.{}\n".format(self.label)
                s += "D;JEQ\n"
                s += "@{}\n".format(self.sp)
                s += "M=0\n"
                s += "@n.{}\n".format(self.label)
                s += "0;JMP\n"
                s += "(eq.{})\n".format(self.label)
                s += "@{}\n".format(self.sp)
                s += "M=1\n"
                s += "@n.{}\n".format(self.label)
                s += "0;JMP\n"            
                s += "(n.{})\n".format(self.label)
                self.label += 1
            if cmd.a1 == "GT":            
                self.sp += -1
                s += "@{}\n".format(self.sp)
                s += "D=M\n"
                self.sp += -1
                s += "@{}\n".format(self.sp)
                s += "D=M-D\n"
                #Jump function that sets x == 1 if x>y
                s += "@eq.{}\n".format(self.label)
                s += "D;JGT\n"
                s += "@{}\n".format(self.sp)
                s += "M=0\n"
                s += "@n.{}\n".format(self.label)
                s += "0;JMP\n"
                s += "(eq.{})\n".format(self.label)
                s += "@{}\n".format(self.sp)
                s += "M=1\n"
                s += "@n.{}\n".format(self.label)
                s += "0;JMP\n"            
                s += "(n.{})\n".format(self.label)
                self.label += 1
            if cmd.a1 == "LT":    
                self.sp += -1
                s += "@{}\n".format(self.sp)
                s += "D=M\n"
                self.sp += -1
                s += "@{}\n".format(self.sp)
                s += "D=M-D\n"
                #Jump function that sets x == 1 if x<y
                s += "@eq.{}\n".format(self.label)
                s += "D;JLT\n"
                s += "@{}\n".format(self.sp)
                s += "M=0\n"
                s += "@n.{}\n".format(self.label)
                s += "0;JMP\n"
                s += "(eq.{})\n".format(self.label)
                s += "@{}\n".format(self.sp)
                s += "M=1\n"
                s += "@n.{}\n".format(self.label)
                s += "0;JMP\n"            
                s += "(n.{})\n".format(self.label)
                self.label += 1
            if cmd.a1 == "AND":
                self.sp += -1
                s += "@{}\n".format(self.sp)
                s += "D=M\n"
                self.sp += -1
                s += "@{}\n".format(self.sp)
                s += "M=D&M\n"
            if cmd.a1 == "OR":
                self.sp += -1
                s += "@{}\n".format(self.sp)
                s += "D=M\n"
                self.sp += -1
                s += "@{}\n".format(self.sp)
                s += "M=D|M\n"
        s += self.changeSP(1)
        return s

    def writeToStack(self, offset):
        s = "@{}\n".format(offset)
        s += "D=M\n"
        s = "@{}\n".format(self.sp)
        s += "M=D\n"
        s += self.changeSP(1)
        return s
    
    def popStack(self, memorySeg, off = 0):
        s = ""
        self.sp += -1
        s += "@{}\n".format(self.sp)
        s += "D=M\n"
        s += "@{}\n".format(memorySeg + int(off))
        s += "M=D\n"
        return s
    
    def staticAssign(self, memorySeg, alloc):
        s = ""
        #push/pop
        s += "@{}.{}\n".format(self.f.split(".")[0], alloc)
        s += "D=M\n"
        s = "@{}\n".format(self.sp)
        s += "M=D\n"
        s += self.changeSP(1)
        return s

    def staticPop(self, memorySeg, alloc):
        s = ""
        #push/pop
        self.sp += -1
        s = "@{}\n".format(self.sp)
        s += "D=M\n"
        s += "@{}.{}\n".format(self.f.split(".")[0], alloc)
        s += "M=D\n"        
        return s
    
    def updatePointer(self, newLoc):
        self.pointer = newLoc
        s = "@{}\n".format(self.pointer)
        return s

    #TODO: separate this for separate push pop write, easier to test
    def writePushPop(self, cmd):
        s = ""
        if cmd.ct == "C_PUSH":
            if cmd.a1 == "CONSTANT":
                s += "@{}\n".format(cmd.a2)
                s += "D=A\n"
                s += "@{}\n".format(self.sp)
                s += "M=D\n"
                s += self.changeSP(1)
            if cmd.a1 == "ARGUMENT":
                s += self.writeToStack(self.arg + int(cmd.a2))
            if cmd.a1 == "THIS":
                s += self.writeToStack(self.pointer + int(cmd.a2))
            if cmd.a1 == "THAT":
                s += self.writeToStack(self.pointer + self.thatOffset + int(cmd.a2))
            if cmd.a1 == "LOCAL":
                s += self.writeToStack(self.lcl + int(cmd.a2))
            if cmd.a1 == "TEMP":
                s += self.writeToStack(self.temp + int(cmd.a2))
            if cmd.a1 == "STATIC":
                s += self.staticAssign(self.static, int(cmd.a2))
        elif cmd.ct == "C_POP":
            if cmd.a1 == "LOCAL":
                s += self.popStack(self.lcl, cmd.a2)
            if cmd.a1 == "THIS":
                s += self.popStack(self.pointer, cmd.a2)
            if cmd.a1 == "THAT":
                s += self.popStack(self.pointer + self.thatOffset, cmd.a2)
            if cmd.a1 == "TEMP":
                s += self.popStack(self.temp, cmd.a2)
            if cmd.a1 == "ARGUMENT":
                s += self.popStack(self.arg, cmd.a2)
            if cmd.a1 == "STATIC":
                s += self.staticPop(self.arg, cmd.a2)
            if cmd.a1 == "POINTER":
                s += self.updatePointer(self.pointer)
        return s

    def writeInit(self):
        self.sp = 256
        self.updateSP()
        self.writeCall("Sys.init", 0)
    
    def writeLabel(self, label, lnum):
        return "({}.{})\n".format(label,lnum)

    
    def writeGoto(self, funcName, label):
        return "{}.{}".format(funcName,label)
    
    def writeIf(self):
        pass
    
    def _pushFrame(self):
        s = ""
        s += self.writePushPop(Command("C_PUSH","CONSTANT", self.arg))
        s += self.writePushPop(Command("C_PUSH", "CONSTANT", self.lcl))
        s += self.writePushPop(Command("C_PUSH", "CONSTANT", self.pointer))
        s += self.writePushPop(Command("C_PUSH", "CONSTANT", self.pointer + self.thatOffset))
        return s
    
    def writeCall(self, funcName, numArgs):
        s = ""
        a = 0
        for i in range(numArgs):
            s += self.writePushPop(Command("C_PUSH","ARG", i))
        #push return address to stack s += "{}.{}\n".format(self.funcName,a)
        s += self.writePushPop(Command("C_PUSH","CONSTANT", "{}.{}".format(self.funcName,a)))
        #push frame of calling function
        s += self._pushFrame()
        #set ARG to sp - n - 5
        s += "@{}\nD=A\n@ARG\nM=D".format(self.sp-numArgs-5)
        #set LCL to sp
        s += "@{}\nD=A\n@LCL\nM=D".format(self.sp)
        s += self.writeGoto(funcName,0)
        #TODO: change up label
        s += self.writeLabel(self.funcName,self.label)
        return
    
    def writeReturn(self):
        # self.funcName = returning function
        s = ""
        # Set Temporary Variable
        s += "@LCL\nD=M\n@FRAME\nM=D\n"
        # Save Return Address
        s += "@FRAME\nD=M\n@5\nD=D-A\n@RET\nM=D\n"
        # Pop return value
        s += self.changeSP(-1)
        s += "@{}\nD=M\n@{}\nM=D".format(self.sp, self.arg)
        s += self.changeSP(1)
        # Restore That
        s += "@FRAME\nD=A\n@1\nD=D-A\n@THAT\nM=D\n"
        # Restore THIS
        s += "@FRAME\nD=A\n@2\nD=D-A\n@THIS\nM=D\n"
        # Restore That
        s += "@FRAME\nD=A\n@3\nD=D-A\n@ARG\nM=D\n"
        # Restore That
        s += "@FRAME\nD=A\n@4\nD=D-A\n@LCL\nM=D\n"
        return
    
    def writeFunction(self, f, k):
        s = ""
        s += self.writeLabel(f,0)
        for i in range(k):
            s += self.writePushPop(Command("C_PUSH", "LOCAL", 0))
        self.funcName = f
        return
        

    def write(self, cmds):
        "Take in a list of commands, sort, and then write out result"
        write_commands = []
        for cmd in cmds:
            if cmd.ct == "C_ARITHMETIC":
                ws = self.writeArithmetic(cmd)
            elif cmd.ct == "C_PUSH" or cmd.ct == "C_POP":
                ws = self.writePushPop(cmd)
            elif cmd.ct == "C_LABEL":
                ws = self.writeLabel(cmd)
            elif cmd.ct == "C_GOTO":
                ws = self.writeGoto(cmd)
            elif cmd.ct == "C_IF":
                ws = self.writeIf()
            elif cmd.ct == "C_FUNCTION":
                ws = self.writeCall()
            elif cmd.ct == "C_RETURN":
                ws = self.writeReturn()
            else:
                pass
            print(ws)
            write_commands.append(ws)
        #rewrite as yield command
        with open(self.f, 'w') as f:
            for string in cmds:
                f.write(string)
        return "OK"
