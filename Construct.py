# ==============================================================================
# File      : Construct.py
# Author    : Max von Hippel and Cole Vick
# Authored  : 30 November 2019 - 13 March 2020
# Purpose   : Constructs and interprets Promela models for Korg.
# How to run: This file is used by Korg.py.
# ==============================================================================
import os
import subprocess
from glob import glob

def makeDaisy(events, N, with_recovery=False, daisyName="daisy.pml", j=0):
	"""
	Scan the model for all send and receive events,
	and their complements. Effectively, this is all 
	the send and receive events possible according to
	the (I/O) interface of the model.
	@param events: the IO interface of the network
	@param N:      model of the network
	@param with_recovery: do we want with_recovery attacks?
	"""
	assert(len(events) != 0)

	network = innerContents(fileRead(N))

	if with_recovery and \
		(network in { False, None } or len(network.strip()) == 0):
		return None

	# TODO: make this bit distinct for each individual process
	# to support multi-process.

	recovery_bitflag = "b"
	while "bit " + recovery_bitflag in network:
		recovery_bitflag = "b" + str(j)
		j += 1
	if j != 0 and recovery_bitflag == "b":
		recovery_bitflag += str(j)

	return network, recovery_bitflag

def makeDaisyWithEvents(events, with_recovery, network, b):
	"""
	Make a daisy using all those ! and ? events. Add
	recovery using the with_recovery flag.
	"""
	daisyname = "daisy" if b == "b" else "daisy_" + b
	daisy = "\nactive proctype " + daisyname + "() {\n\tdo"
	if with_recovery:
		daisy = "\nbit " + b + "= 0;\n" + daisy
	for event in events:
		daisy += "\n\t:: " + event
	if with_recovery:
		daisy += "\n\t:: break; // recovery to N ... \n\tod"
		daisy += "\n\t" + b + " = 1;\n\t"
		# Add recovery to N
		daisy += "// N begins here ... \n" + network + "\n}"
	else:
		daisy += "\n\tod\n}"
	return daisy

def makeDaisyPhiFinite(label, phi):
	"""
	Given a label and LTL spec, creates a new phi that should be 
	satisfied by the daisy.
	@param label: labels??
	@param phi: specification for the daisy
	"""
	phiBody = innerContents(fileRead(phi))
	newPhi = "ltl newPhi {\n\t(eventually ( "
	if isinstance(label, set):
		# TODO
		newPhi += " && ".join([l + " == 1" for l in label])
		newPhi += " ) ) "
	else:
		newPhi += label + \
		     " == 1 ) ) "
	return newPhi + "implies (\n\t\t" + phiBody + "  )\n}"

def makeAttacker(events, prov, net, DIR=None, with_recovery=True, k=0):
	"""
	Create the attacker string given the events that the 
	daisy made. This method also writes the string to a 
	file provided one doesn't already exist.

	@param prov: how spin was executed to return this process

	example of multi (that is, distributed) events:
	[
	  [['q02p ! a'], []], 
	  [['q22p ! c'], []], 
	  [['q12p ! b'], []]
	]
	example of single (that is, centralized) events:
	[
		['q02p ! a'], []
	]
	"""

	# this would make a type theorist faint ...
	iscentralized = isinstance(events[0][0], str)

	names = []

	if iscentralized == True:

		events = [events]

	j = 0

	for attackersevents in events:

		print("Writing attacker " + str(j))

		assert(j == 0 or not iscentralized)

		acyclicEvents, cyclicEvents = attackersevents[0], attackersevents[1]
		acyclicEvents = acyclicEvents if len(acyclicEvents) > 0 else [ "skip" ]

		attackername = "attacker" if iscentralized else "attacker_" + str(j)
		
		proc = "active proctype " + attackername + "() {\n\t"
		
		for ae in acyclicEvents:
			proc += "\n\t" + ae  + ";"
		name = None
		if with_recovery:
			proc += "\n// recovery to N\n// N begins here ... \n" + net + "\n}"
		else:
			proc += "\n\t// Acceptance Cycle part of attack" 
			if len(cyclicEvents) > 0:
				proc += "\n\tdo\n\t::" \
					 + "".join(["\n\t   " + ce + ";" for ce in cyclicEvents]) \
					 + "\n\tod"
			proc += "\n}"
		
		attackerfilename = attackername + "_"                  \
					 + str(k)                                  \
					 + ("_WITH_RECOVERY" * int(with_recovery)) \
					 + ".pml"

		name = (DIR + "/") * int(DIR != None) + attackerfilename

		# Only write the attacker if it isn't a duplicate, as
		# determined using our hash function naming convention.

		if (DIR != None and not os.path.exists(DIR)):
			os.mkdir(DIR)

		if not os.path.exists(name):
			with open(name, "w") as fw:
				fw.write("/* " + " ".join(prov) + " */\n")
				fw.write(proc)

		names.append(attackerfilename)

		j += 1

	return names

def innerContents(singleModelBody):
	"""
	This method returns the body of the given 
	model, as an array. The body is between the 
	two curly brace { }. 
	We assume no comments in the model at the moment ... 
	same with in the properties.
	"""
	if singleModelBody == False:
		return False
	i, j = 0, len(singleModelBody) - 1
	while (singleModelBody[i] != "{" and i < len(singleModelBody)):
		i += 1
	while (singleModelBody[j] != "}" and j > 0):
		j -= 1
	if (i >= j or singleModelBody[i] != "{" or singleModelBody[j] != "}"):
		return None
	return singleModelBody[i+1:j]


def writeAttacks(attacks, provenance, net, with_recovery=True, name="run"):
	"""
	Write given attacks to named directory, provided it doesn't
	already exist.

	[
	  [
	    [['q02p ! a'], []], 
	    [['q22p ! c'], []], 
	    [['q12p ! b'], []]
	  ]
	]
	"""
	name = "out/" + name
	if (not os.path.isdir("out")):
		os.mkdir("out")
	assert(not os.path.isdir(name))
	os.mkdir(name)
	for j in range(len(attacks)):
		_ = makeAttacker(                  \
			events        = attacks[j],    \
			prov          = provenance[j], \
			net           = net,           \
			DIR           = name,          \
			with_recovery = with_recovery, \
			k             = j)

def negateClaim(phi):
	"""
	Given a path to a given LTL specificiationm, phi, negate
	phi and write it to a file called "negated.pml".
	"""
	contents = fileRead(phi)
	if contents == None or contents == False:
		return False
	negated  = False
	with open("negated.pml", "w") as fw:
		for l in contents:
			fw.write(l)
			if (not negated) and l == "{":
				fw.write("!")
				negated = True
	return negated

def getIO(IOfile):
	'''
	Given an IO specification for a network, Q, return 
	a list of the input and output events. 

	format is like ...

	[chanName]:
		I: [inputs]
		O: [outputs]
	'''
	if os.path.isdir(IOfile):
		return [getIO(f) for f in glob(IOfile + "/IO*.txt")]
	# else is a file
	events = set()
	chan   = None
	lineType = lambda x : 2 if "O:" in x else 1 if "I:" in x else 0
	try:
		with open(IOfile, "r") as fr:
			for line in fr:
				j = lineType(line)
				parts = [a.strip() for a in line.split(":")]
				parts = [p for p in parts if len(p) > 0]
				if j == 0:
					chan = parts[0]
					continue
				part2 = [] if len(parts) < 2 else \
						[a.strip() for a in parts[1].split(",")]
				part2 = list(set(part2))
				for msg in part2:
					if j == 1 and chan != None:
						events.add(chan + "?" + msg + ";")
					elif j == 2 and chan != None:
						events.add(chan + "!" + msg + ";")
		return events
	except Exception:
		return None

def fileRead(fileName):
	try:
		txt = None
		with open(fileName, 'r') as fr:
			txt = fr.read()
		return txt
	except Exception:
		return False
		
def writeDaisyToFile(daisy_string, file_name):
	with open(file_name, "w") as fw:
		fw.write(daisy_string)