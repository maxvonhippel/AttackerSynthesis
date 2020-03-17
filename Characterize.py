# ==============================================================================
# File      : Characterize.py
# Author    : Max von Hippel and Cole Vick
# Authored  : 30 November 2019 - 13 March 2020
# Purpose   : Checks when models do or do not satisfy properties.  Also inter-
#             prets various outputs of Spin.
# How to run: This code is used by Korg.py, which is what you want to run.
# ==============================================================================

import subprocess
import sys
import os
from   glob import glob

'''
Given the path to a model containing one or more properties,
checks if that model violates one or more of those properties.

INPUT:
	modelFile - the string containing the path to the model file
OUTPUT:
	true iff modelFile runs successfully without acceptance cycles
	or violations else false
'''
def check(modelFile, maxDepth=10000):
	if maxDepth > 10000 * 20:
		print("maxDepth too large for any realistic run.  Edit the code if " \
			+ "you actually really want to do this ... in Characterize.py.")
		return False
	args = "spin -run -a -m" + str(maxDepth) + " -RS88 " + modelFile
	args = [a.strip() for a in args.split(" ")]
	args = [a for a in args if len(a) > 0]
	ret = None
	with open(os.devnull, 'w') as devnull:
		try:
			ret = subprocess.check_output(args, stderr=devnull)
			if sys.stdout.encoding != None:
				ret = ret.decode(sys.stdout.encoding).strip()
			else:
				ret = str(ret)
		except Exception as e:
			raise e
	if ret == None:
		return False
	if "depth too small" in ret:
		print("Search depth was too small at " + str(maxDepth), " doubling depth ...")
		return check(modelFile, maxDepth * 2)
	return not ("violated" in ret or "acceptance cycle" in ret)

def makeAllTrails(modelFile, numTrails=100):
	args = ""
	if numTrails <= 1:
		args = "spin -run -a " + modelFile
	else:
		args = "spin -run -a -e -c" + str(numTrails - 1) + " " + modelFile
	subprocess.run(args.split(" "))
	
'''
Given the paths to a model and a property, checks if that 
model makes true that property.

INPUT:
	model - the string containing the path to the model file
	phi   - the string containing the path to the ltl model file
	N     - the string containing the path to the N model file
OUTPUTS:
	true iff the model (model || phi || N) runs successfully without
	acceptance cycles or violations else false
'''
def models(model, phi, N, name):
	
	if None in { model, phi, N, name }:
		return False
	
	fmrLines = ""
	fNrLines = ""
	fprLines = ""
	
	with open(model, 'r') as fmr:
		fmrLines = fmr.read()

	with open(N, 'r') as fNr:
		fNrLines = fNr.read()

	with open(phi, 'r') as fpr:
		fprLines = fpr.read()

	with open(name, 'w') as fw:
		fw.write(fmrLines + "\n" + fNrLines + "\n" + fprLines)

	assert(os.path.isfile(name))

	return check(name)

# Example snippet of what sort of text parseTrail parses:
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
def parseTrail(trailBody):

	ret, i = [[], []], 0

	for line in trailBody.split("\n"):

		if "(daisy:" in line:

			# https://stackoverflow.com/a/29571669/1586231
			LL = line.rstrip("*")
			chan = LL[line.rfind("(")+1:-1]
			msg, evt = None, None
			
			if "Recv " in line:
			
				msg = LL[line.rfind("Recv ")+5:].split()[0]
				evt = "?"
			
			elif "Send" in line:
			
				msg = LL[line.rfind("Send ")+5:].split()[0]
				evt = "!"
			
			if evt != None and msg != None:

				ret[i].append(chan + " " + evt + " " + msg)
		
		elif "CYCLE" in line:
			i = 1
	
	return ret

def parseAllTrails(cmds, with_recovery=False, debug=False):
	ret = []
	prov = []
	with open(os.devnull, 'w') as devnull:
		for cmd in cmds:
			output = subprocess.check_output(cmd, stderr=devnull)
			if sys.stdout.encoding != None:
				output = output.decode(sys.stdout.encoding)
			output = str(output).strip().replace("\\n", "\n").replace("\\t", "\t")
			parsed = parseTrail(output)
			ret.append(parsed)
			prov.append(cmd)
	return ret, prov

def attackType(A, E):
	# if A == 1 then E == 1
	# <=> not (A == 1 and E == 0)
	assert(not (A and not E))
	if A:
		return "A-attack"
	if E:
		return "E-attack"
	return "NOT AN ATTACK"

def characterizeAttacks(model, phi, with_recovery=True, name="run"):
	assert(os.path.isdir("out/" + name))
	nE, nA = 0, 0
	with open("out/" + name + "/log.txt", "w") as fw:
		if not (os.path.isdir("out/" + name + "/artifacts")):
			os.mkdir("out/" + name + "/artifacts")
		fw.write("model,A/E,with_recovery?\n")
		for attackModel in glob("out/" + name + "/attacker*.pml"):
			# is it a forall attack?
			attackName = os.path.basename(attackModel).replace(".pml", "")
			aName = "out/" + name + "/artifacts/" + attackName + "_A.pml"
			eName = "out/" + name + "/artifacts/" + attackName + "_E.pml"
			A = (models(model, "negated.pml", attackModel, aName) == True )
			E = (models(model, phi,           attackModel, eName) == False)
			if A:
				nA += 1
			elif E:
				nE += 1
			fw.write(",".join([ \
				attackModel, attackType(A, E), str(with_recovery)]) + "\n")
	return (nE, nA)