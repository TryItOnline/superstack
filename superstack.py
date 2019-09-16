##############
# Super Stack!
# v2
# 8/18/09
##############
# changes from v1:
#  o output command now adds space after number
#    instead of newline
#  o added random keyword
##############
# Make a note of bugs you find on the wiki!

import sys,random

def run(text,debug=0):
    prog = [line.lower()
            for line in text.replace('\t',' ').replace('\n',' ').strip().split(' ')
            if line!=''] #Hack and slash the text to put each keyword in an element on a list
    if debug:print 'running:\n',prog

    stack = [] #The stack
    jump_stack = [] #The jump stack for if-fi loops

    pc = 0 #program counter

    while pc<len(prog):
        inst = prog[pc]
        if debug:print pc,':',inst

        #Numbers
        try:
            stack.append(int(inst))
        except:
            pass

        #Math
        if   inst=='add':stack.append(stack.pop()+stack.pop())
        elif inst=='sub':
            a,b = stack.pop(),stack.pop()
            stack.append(b-a)
        elif inst=='mul':stack.append(stack.pop()*stack.pop())
        elif inst=='div':
            a,b = stack.pop(),stack.pop()
            stack.append(int(b/a))
        elif inst=='mod':
            a,b = stack.pop(),stack.pop()
            stack.append(b%a)
        elif inst=='random': stack.append(random.randrange(stack.pop()))

        #Logic
        elif inst=='and':
            stack.append(int(
                bool(stack.pop()) and bool(stack.pop())
                ))
        elif inst=='or':
            stack.append(int(
                bool(stack.pop()) or bool(stack.pop())
                ))
        elif inst=='not':
            stack.append(int(bool(not stack.pop())))
        elif inst=='xor':
            stack.append(int(
                not (bool(stack.pop()) or bool(stack.pop()))
                ))
        elif inst=='nand':
            stack.append(int(
                not (bool(stack.pop()) and bool(stack.pop()))
                ))

        #I/O
        elif inst=='output':sys.stdout.write(str(stack.pop())+' ')
        elif inst=='input':stack.append(int(raw_input('?')))
        elif inst=='outputascii':sys.stdout.write(chr(stack.pop()))
        elif inst=='inputascii':stack.extend(map(ord,raw_input(''))[::-1]) #Ah, slice steps

        #Stack manipulation
        elif inst=='pop':stack.pop()
        elif inst=='swap':
            a,b = stack.pop(),stack.pop()
            stack.extend([a,b])
        elif inst=='cycle':stack.insert(0,stack.pop())
        elif inst=='rcycle':
            stack.append(stack[0])
            del stack[0]
        elif inst=='dup':
            a = stack.pop()
            stack.append(a)
            stack.append(a)
        elif inst=='rev':stack.reverse()

        #Flow
        elif inst=='quit':return
        elif inst=='if': #While loop
            if stack[-1]!=0: #If top number true, keep going in the loop
                jump_stack.append(pc-1)
            else: #Else, skip ahead to matching fi keyword
                loop = 1
                while loop:
                    pc += 1
                    inst = prog[pc]
                    if inst=='if':
                        loop += 1
                    elif inst=='fi':
                        loop -= 1
        elif inst=='fi': pc = jump_stack.pop()

        #Misc
        elif inst=='debug':print stack
        pc+=1

    if stack and debug:
        print'program ended with not empty stack:\n',stack

def usage():
    print 'superstack.py my_program.ss! [-d]'
    print '    -d  debug'
    sys.exit(2)
try:
    from string import join
    run(
        open(sys.argv[1]).read(),
        '-d' in sys.argv #debug
    )
except IOError:
    print'Can not read file',sys.argv[1]
except IndexError:
    usage()

