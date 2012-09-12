#!/usr/bin/python
import sys
#TODO
#DONE nested blocks...oh noes
#oh and i guess multiple blocks in general just dont work either
#DONE executing if blocks only IF cond is true
variables = {}
block = ""
def myeval(exps):
    brackount = 0
    foundbrack = False
    backup = exps
    if "{" in backup:
        blockstart = backup.index("{") #goes to shit with > 1 unrelated blocks
        blockend = 0
        for i in range(len(backup)):
            if foundbrack and brackount == 0:
                break
            if backup[i] == "{":
                foundbrack = True
                brackount += 1
            if backup[i] == "}":
                brackount -= 1
                blockend = i
        block = backup[blockstart:blockend+1]
        exps = exps.replace(block,"@block;")
        


    exps = exps.split(";")

    lastval = exps[-1]
    
    if len(exps) > 1:
        exps.remove(lastval)
    for exp in exps:
        exp = exp.replace("\n","")
      
        if len(exp.split()) < 1:
            break
        if assignment(exp): 
            eval_assignment(exp)
        if is_display(exp): 
            eval_display(exp) 

        exp = exp.split(":")

        if is_if(exp):
            eval_if(exp,block)
        
        if is_while(exp):
            eval_while(exp,block)



def is_if(exp):
    if len(exp) > 1:    
        if 'if' in exp[0]:
            return True


def eval_if(exp,block):
    if type(block) == str:
        listblock = [char for char in block]
        listblock[listblock.index("{")] = ""
        listblock[max([i for i in range(len(listblock)) if listblock[i] == "}"])] = ""
        block = ""
        for char in listblock:
            block += char
        if "while" in block:
            innerblockstart = block.index("while")
            innerblockend = block.rindex("}")
            innerblock = block[innerblockstart:innerblockend+1]
            block = block.replace(innerblock,"@block;")
        block = block.replace("\n","")
        block = block.split(";")
    operator = None
    cond = exp[0][exp[0].index("if")+len("if "):]
    for op in oplist:
        if op in cond:
            operator = op
    if assess(operator,cond[:cond.index(operator)],cond[cond.index(operator)+len(operator):]):
        for line in block:
            if "@block" in line:
                myeval(innerblock)
            myeval(line)
        #myeval(exp[1][1:].replace("{","").replace("}",""))


def assess(operator,op1,op2):
    if operator == ">":
        return simplify(op1) > simplify(op2)
    if operator == "<":
        return simplify(op1) < simplify(op2)
    if operator == "==":
        return simplify(op1) == simplify(op2)


def is_while(exp):
    if len(exp) > 1:
        if 'while' in exp[0]:
            return True

oplist = ["<",">","=="]

def eval_while(exp,block):
    if type(block) == str:
        listblock = [char for char in block]
        listblock[listblock.index("{")] = ""
        listblock[max([i for i in range(len(listblock)) if listblock[i] == "}"])] = ""
        block = ""
        for char in listblock:
            block += char
        if "while" in block:
            innerblockstart = block.index("while")
            innerblockend = block.rindex("}")
            innerblock = block[innerblockstart:innerblockend+1]
            block = block.replace(innerblock,"@block;")

        block = block.replace("\n","")
        block = block.split(";")
    cond = exp[0][exp[0].index('while')+len("while "):]
    operator = None
    for op in oplist:
        if op in cond:
            operator = op
    if assess(operator,cond[:cond.index(operator)],cond[cond.index(operator)+len(operator):]):
        for line in block:
            if "@block" in line:
                try:
                    myeval(innerblock)
                except:
                    pass
            myeval(line)
        print exp,block
        return eval_while(exp,block)

def is_display(exp):
    exp = exp.split()
    if exp[0] == "display":
        return True

def eval_display(exp):
    val = simplify(exp[exp.index("display ")+len("display "):])
    print val


def assignment(exp):
    if '=' in exp:
        return True

def eval_assignment(exp):
    var,val = exp.split("=")[0], exp.split("=")[1] 
    variables[var.replace(" ","")] = simplify(val)

def number(exp):
    try:
        int(exp)
        return True
    except:
        return False
    
def string(exp):
    if '"' in exp:
        for char in exp[:exp.index('"')]:
            if char != " ":
                return False
        if exp[-1] == '"':
            return True

def simplify(exp):
    if string(exp):
        return exp
    exp = exp.replace(" ","")
    exp = exp.replace("{","")
    exp = exp.replace("}","")
    if number(exp):
        return int(exp)
    if exp in variables:
        return variables[exp]
    else:
        if "<" in exp:
            front,back = exp[:exp.index("<")],exp[exp.index("<")+1:]
            return simplify(front) < simplify(back)
        if ">" in exp:
            front,back = exp[:exp.index(">")],exp[exp.index(">")+1:]
            return simplify(front) > simplify(back)
        if "+" in exp:
            front,back = exp[:exp.index("+")],exp[exp.index("+")+1:]
            return simplify(front) + simplify(back)
        if "-" in exp:
            front,back = exp[:exp.index("-")],exp[exp.index("-")+1:]
            return simplify(front) - simplify(back)
        if "*" in exp:
            front,back = exp[:exp.index("*")],exp[exp.index("*")+1:]
            return simplify(front) * simplify(back)
        if "/" in exp:
            front,back = exp[:exp.index("/")],exp[exp.index("/")+1:]
            return simplify(front) / simplify(back)
        if "%" in exp:
            front,back = exp[:exp.index("%")],exp[exp.index("%")+1:]
            return simplify(front) % simplify(back)


#myeval("""hello = "hi everybody";
 #         display "5+4";
 #         x = 1;
  #        if 4<3: {display "hello"};
   #       if 1<2: {display "penis"};
         
    #      """)


fil = sys.argv[1]
fi = ""
with open(fil,'r') as f:
    f = f.readlines()
    for line in f:
        fi += line
    myeval(fi)




