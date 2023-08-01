#!/usr/bin/env python3

import sys


debug=False
if len(sys.argv)>2:
    debug=True

# read whole program
prgm=None
fn=sys.argv[1]
with open(fn,'r') as f:
    prgm=f.read()

ip=0 # instruction pointer
s=[] # stack
var={} # variables
d=0 # bracket depth

def breakout():
    # break out of the [ ... ] loop
    global d
    global ip
    if debug:
        print(f"Breaking out of loop: Setting depth from {d} to ",end='')
    cd=d # current depth
    while d>=cd:
        ip+=1
        if prgm[ip]=='[':
            d+=1
        if prgm[ip]==']':
            d-=1
    if debug:
        print(d)

# too lazy to write a lexer, I'll just read character-wise and add strings
# of digits up to the number they represent
n=None # number that is currently being built
while ip<len(prgm):

    # read char
    c=prgm[ip]

    # 123: Push the natural number (includes 0) onto the stack. (There is an infinite number of natural numbers.)
    if c>='0' and c<='9':
        # build a number
        if n is None:
            n=0
        n=10*n+(ord(c)-48)
    elif n is not None:
        # push finished number onto the stack
        s.append(n)
        n=None

    # s: Successor function: Pops a, pushes a+1.
    if c=='s':
        s.append(s.pop()+1)

    # ,: Pops a and v. Store a to the variable numbered v. (If there is no a on the stack, break out of the [ ... ] loop.)
    if c==',':
        a=s.pop()
        if len(s)>0:
            v=s.pop()
            var[a]=v
        else:
            # If there is no a, break out of the [ ... ] loop
            breakout()

    # !: Pops v. Push the value of the variable numbered v onto the stack.
    if c=='!':
        v=s.pop()
        s.append(var[v])

    # [ ... ]: Infinite loop: Executes ... forever.
    if c=='[':
        d+=1
    if c==']':
        if debug:
            print(f"Looping: Setting ip from {ip} back to ",end='')
        cd=d # current depth
        x=cd # temporary variable - We stay in the loop, so depth doesn't change!
        while x>=cd:
            ip-=1
            if prgm[ip]==']':
                x+=1
            if prgm[ip]=='[':
                x-=1
        if debug:
            print(ip)

    # =: Pops a and b. If a and b are equal, break out of the [ ... ] loop.
    if c=='=':
        a=s.pop()
        b=s.pop()
        if a==b:
            breakout()

    # advance
    if debug and c in "[]0123456789,!s=":
        # print state and wait for user to give okay to advance
        input(f"ip={ip} c='{c}' d={d} s={s} var={var}")
    ip+=1

# push lastly built number to the stack
if n is not None:
    s.append(n)
    n=None

# print stack
print(f"Done. Stack: {s} Vars: {var}")
