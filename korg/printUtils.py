'''
name       : printUtils.py
author     : [redacted]
authored   : 9 June 2020, directly ripped from RFCNLP code.
description: provides pretty-print utils
'''

class bcolors:
    HEADER    = '\033[95m'
    OKBLUE    = '\033[94m'
    OKGREEN   = '\033[92m'
    WARNING   = '\033[93m'
    FAIL      = '\033[91m'
    ENDC      = '\033[0m'
    BOLD      = '\033[1m'
    UNDERLINE = '\033[4m'


# A print utility that only prints if debug=True
def debugPrint(string, debug=False):
	if debug:
		print(f"{bcolors.WARNING}{string}{bcolors.ENDC}")

def printTransition(transition, delta1=15, delta2=20):
    (a, B, c) = transition
    BB = ";".join(B) if not (str(type(B)) == "<class 'str'>") else B
    
    prefix  = str(a)
    inner   = " ---"  + BB
    postfix = "---> " + str(c)

    prefix_to_inner_pad  = max(0, delta1 - len(prefix)) * " "
    inner_to_postfix_pad = max(0, delta2 - len(inner) ) * " "

    return prefix + prefix_to_inner_pad + inner + inner_to_postfix_pad + postfix

def makeGreen(str):
    return f"{bcolors.OKGREEN}{str}{bcolors.ENDC}"

def makeRed(str):
    return f"{bcolors.WARNING}{str}{bcolors.ENDC}"

def makeBlue(str):
    return f"{bcolors.OKBLUE}{str}{bcolors.ENDC}"

def makeBold(str):
    return f"{bcolors.BOLD}{str}{bcolors.ENDC}"

def makeFail(str):
    return f"{bcolors.FAIL}{str}{bcolors.ENDC}"