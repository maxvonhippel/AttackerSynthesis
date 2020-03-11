'''
							CLI.py
				Authored 30 November 2019 by Max von Hippel
PURPOSE:

	This file contains code used to delete files / clean up,
	get command-line inputs, create new Bash commands to
	be executed, and output information to the user.

'''

import argparse
from   glob import glob
import os

def str2bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

def getArgs():
	parser = argparse.ArgumentParser(
		description='Synthesize a (P, phi)-Attacker.')
	parser.add_argument(
		'--model', 
		metavar='model', 
		type=str, 
		help='A relative or absolute path to a Promela model of a protocol M \
			  to be attacked, e.g. demo/TCP.pml.')
	parser.add_argument(
		'--phi', 
		metavar='phi', 
		type=str, 
		help='A relative or absolute path to a Promela file containing an LTL \
			  claim phi about M and N, such that (M || N) |= phi, e.g. \
			  demo/noHalfOpenConnections.pml.')
	parser.add_argument(
		'--Q',
		metavar='Q',
		type=str,
		help='A relative or absolute path to a Promela model of a protocol Q \
			  to be replaced and recovered-to by our attacker, e.g. \
			  demo/network.pml.')
	parser.add_argument(
		'--IO',
		metavar='IO',
		type=str,
		help='The input-output interface of N, in a yaml-ish format.')
	parser.add_argument(
		'--max_attacks',
		metavar='max_attacks',
		type=int,
		help='The maximum number of attackers to generate.')
	parser.add_argument(
		'--finite',
		metavar='finite',
		type=str2bool,
		default=False,
		nargs='?',
		const=True,
		help='True iff you want to solve the F∃ASP, False iff you want to solve the ∃ASP.')
	parser.add_argument(
		'--name',
		metavar='name',
		type=str,
		help='The name you want to give to this experiment.')
	parser.add_argument(
		'--characterize',
		metavar='characterize',
		type=str2bool,
		default=False,
		nargs='?',
		const=True,
		help='True iff you want the tool to tell you if the results are ' \
			+ 'A-, E-, or not attackers at all.  May substantially add to runtime!')

	args = parser.parse_args()
	return args

trails = lambda : glob("*.trail")

def cleanUpTargeted(target):
	files = glob(target)
	for file in files:
		os.remove(file)

def cleanUp(func):
	def wrapped():
		a = func()
		cleanUpTargeted("*.trail")
		cleanUpTargeted("*tmp*"  )
		cleanUpTargeted("pan"    )
		return a
	return wrapped

def addTrailNumberToArgs(args, num):
	ret = []
	for arg in args:
		if arg != "-t":
			ret.append(arg)
		else:
			ret.append(arg + str(num))
	return ret

def handleTs(args, name):
	print("\n\n\nCALLING HANDLE Ts\n\n\n")
	args = args.split(" ")
	num  = len(glob(name + "*.trail"))
	if num == 0:
		print("NUM = 0 ... @MAX")
		return []
	elif num == 1:
		print("NUM = 1 this is a problem ... @MAX")
		return [args]
	else:
		print("Debug addTrailNumberToArgs .... @MAX")
		return [addTrailNumberToArgs(args, i) for i in range(0, num)]

'''
(env) mvh:attempt2$ spin -t -s -r 956233795109139376_tmp.pml
ltl exp3: (! ([] (<> (((state[0]==1)) && ((state[1]==2)))))) || (<> ((state[0]==4)))
starting claim 3
Never claim moves to line 4	[(!((state[0]==4)))]
  2:	proc  1 (daisy:1) 956233795109139376_tmp.pml:93 Send SYN_ACK	-> queue 1 (NtoB)
  4:	proc  1 (daisy:1) 956233795109139376_tmp.pml:94 Send SYN_ACK	-> queue 2 (NtoA)
 34:	proc  3 (TCP:1) 956233795109139376_tmp.pml:24 Send SYN	-> queue 4 (snd)
Never claim moves to line 3	[((!((state[0]==4))&&((state[0]==1)&&(state[1]==2))))]
 38:	proc  3 (TCP:1) 956233795109139376_tmp.pml:42 Recv SYN_ACK	<- queue 1 (rcv)
Never claim moves to line 8	[(!((state[0]==4)))]
 40:	proc  1 (daisy:1) 956233795109139376_tmp.pml:96 Recv SYN	<- queue 4 (BtoN)
Never claim moves to line 3	[((!((state[0]==4))&&((state[0]==1)&&(state[1]==2))))]
 42:	proc  3 (TCP:1) 956233795109139376_tmp.pml:42 Send ACK	-> queue 4 (snd)
Never claim moves to line 8	[(!((state[0]==4)))]
Never claim moves to line 4	[(!((state[0]==4)))]
 46:	proc  1 (daisy:1) 956233795109139376_tmp.pml:92 Recv ACK	<- queue 4 (BtoN)
 48:	proc  3 (TCP:1) 956233795109139376_tmp.pml:54 Send FIN	-> queue 4 (snd)
 52:	proc  1 (daisy:1) 956233795109139376_tmp.pml:100 Recv FIN	<- queue 4 (BtoN)
 54:	proc  1 (daisy:1) 956233795109139376_tmp.pml:106 Send FIN	-> queue 1 (NtoB)
 56:	proc  3 (TCP:1) 956233795109139376_tmp.pml:62 Recv FIN	<- queue 1 (rcv)
 58:	proc  3 (TCP:1) 956233795109139376_tmp.pml:62 Send ACK	-> queue 4 (snd)
 62:	proc  1 (daisy:1) 956233795109139376_tmp.pml:92 Recv ACK	<- queue 4 (BtoN)
 64:	proc  1 (daisy:1) 956233795109139376_tmp.pml:107 Send ACK	-> queue 1 (NtoB)
 66:	proc  3 (TCP:1) 956233795109139376_tmp.pml:74 Recv ACK	<- queue 1 (rcv)
 76:	proc  1 (daisy:1) 956233795109139376_tmp.pml:102 Send SYN	-> queue 1 (NtoB)
'''
def trailParseCMDs(tmpName):
	args = "spin -t -s -r " + tmpName
	return handleTs(args, tmpName)

# Error message for if we were handed apparently invalid inputs.
def printInvalidInputs(model, phi, N, TESTING=False):
	if TESTING:
		return
	print("In order for the problem (model, phi, N) to be non-trivial, we \
		   require that (model || N) |= phi.  However, this does not appear \
		   to be the case.")

# Error message for if we cannot find any solution.
def printNoSolution(model, phi, N, finite, TESTING=False):
	if TESTING:
		return
	possiblyFinite = "finite" if finite else ""
	print("We could not find any " + possiblyFinite + "(model, (N), phi)-attacker A.")

# Error message when we could not negate the claim phi.
def printCouldNotNegateClaim(phi, TESTING=False):
	if TESTING:
		return
	if phi == None:
		print("No property phi provided; giving up.")
	else:
		print("We could not negate the claim in " + phi + "; giving up.")

# Error message when we could not get any inputs or outputs.
def printZeroIO(IO, TESTING=False):
	if TESTING:
		return
	print("We could not find any inputs or outputs in " + IO + "; giving up.")

# Error message when num is too small
def printInvalidNum(num, TESTING=False):
	if TESTING:
		return
	print("--num option must be > 0, was: " + str(num) + "; giving up.")