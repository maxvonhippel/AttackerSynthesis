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
		print("Search depth was too small at " \
			 + str(maxDepth), \
			 " doubling depth ...")
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
	
	if None == model or \
	   None == phi   or \
	   None == N     or \
	   None == name:

		return False
	
	fmrLines, fNrLines, fprLines = "", "", ""

	with open(model, 'r') as fmr:
		fmrLines = fmr.read()

	if isinstance(N, list):
		for _N in N:
			with open(_N, 'r') as fNr:
				fNrLines += fNr.read()
	elif os.path.isfile(N):
		with open(N, 'r') as fNr:
			fNrLines = fNr.read()
	else:
		if not os.path.isdir(N):
			print("Something is wrong with " + str(N))
			return False
		for _N in glob(N + "/*.pml"):
			with open(_N, 'r') as fNr:
				fNrLines += fNr.read()

	with open(phi, 'r') as fpr:
		fprLines = fpr.read()

	with open(name, 'w') as fw:
		fw.write(fmrLines + "\n" + fNrLines + "\n" + fprLines)

	assert(os.path.isfile(name))

	return check(name)

# Parses output of reading trail using Spin.
def parseTrail(trailBody, components=1, name="daisy"):

	if components > 1:
		return [parseTrail(trailBody, 1, name + "_b" + str(i + 1)) \
		        for i in range(components)]

	ret, i = [[], []], 0

	for line in trailBody.split("\n"):

		if "(" + name + ":" in line:

			# https://stackoverflow.com/a/29571669/1586231
			LL = line.rstrip("*")
			chan = LL[line.rfind("(") +1 : -1]
			msg, evt = None, None
			
			if "Recv " in line:
			
				msg = LL[line.rfind("Recv ") + 5 :].split()[0]
				evt = "?"
			
			if "Send" in line and msg == None and evt == None:
			
				msg = LL[line.rfind("Send ") + 5 :].split()[0]
				evt = "!"

			if "Sent" in line and msg == None and evt == None:
			
				msg = LL[line.rfind("Sent ") + 5 :].split()[0]
				evt = "!"
			
			if evt != None and msg != None:

				ret[i].append(chan + " " + evt + " " + msg)
		
		elif "CYCLE" in line:
			i = 1
	
	return ret

def parseAllTrails(cmds, with_recovery=False, debug=False, components=1):
	ret = []
	prov = []
	with open(os.devnull, 'w') as devnull:
		for cmd in cmds:
			output = subprocess.check_output(cmd, stderr=devnull)
			if sys.stdout.encoding != None:
				output = output.decode(sys.stdout.encoding)
			output = str(output).strip().replace("\\n", "\n")\
										.replace("\\t", "\t")
			parsed = parseTrail(output, components)
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

def characterizeAttacks(\
	model, phi, with_recovery=True, name="run", distributed=False):

	nE, nA = 0, 0

	with open("out/" + name + "/log.txt", "w") as fw:

		if not (os.path.isdir("out/" + name + "/artifacts")):
			os.mkdir("out/" + name + "/artifacts")

		fw.write("model,A/E,with_recovery?\n")

		if distributed:

			j = 0
			while True:
				components = glob("out/" + name + "/attacker_*_" + str(j) + "_*.pml")
				if len(components) == 0:
					break
				attackName = name + "_" + str(j)
				aName = "out/" + name + "/artifacts/" + attackName + "_A.pml"
				eName = "out/" + name + "/artifacts/" + attackName + "_E.pml"
				A = (models(model, "negated.pml", components, aName) == True )
				E = (models(model, phi,           components, eName) == False)
				if A:
					nA += 1
				elif E:
					nE += 1
				fw.write(",".join([ \
					attackName, attackType(A, E), str(with_recovery)]) + "\n")
				j += 1

		else:

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