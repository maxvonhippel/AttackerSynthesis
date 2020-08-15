# ==============================================================================
# File      : Korg.py
# Author    : Max von Hippel and Cole Vick
# Authored  : 30 November 2019 - 13 March 2020
# Purpose   : Primary runner for Korg tool
# How to run: see docs/Korg.md for instructions
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# Security  : This code is not even remotely cyber-secure and should only be run 
#             locally on inputs you personally manufactured.  Otherwise you 
#             expose yourself to a basically trivial remote code execution issue 
#             in Bash, because of the way I am hacking on subprocess.
# ==============================================================================


from CLI          import *
from Characterize import *
from Construct    import *
from glob 		  import glob

def main():
	args = getArgs()
	model, phi, Q, IO, max_attacks, with_recovery, name, characterize \
		= parseArgs(args)
	r = body(model, phi, Q, IO, max_attacks, \
				with_recovery, name, characterize)
	print("r = ", r)
	return r

def parseArgs(args):
	P, Q, IO, phi = (None,) * 4
	if args.dir:
		demo_items = glob(args.dir)
		for item in demo_items:
			if 'P.pml' in item:
				P = item
			elif 'Q.pml' in item:
				Q = item
			elif 'Phi.pml' in item:
				phi = item
			elif 'IO.txt' in item:
				IO = item
	else:
		P, Q, IO, phi = args.model, args.Q, args.IO, args.phi
	return P, 	            \
		phi, 		        \
		Q, 		            \
		IO,                 \
		args.max_attacks,   \
		args.with_recovery, \
		args.name,          \
		args.characterize

def checkArgs(max_attacks, phi, model, Q, basic_check_name, IO):
	if max_attacks == None or max_attacks < 1:
		printInvalidNum(max_attacks)
		return 1

	# Can we negate phi?  This is important.
	if not negateClaim(phi):
		printCouldNotNegateClaim(phi)
		return 2

	print("Successfully negated claim phi ...")
	
	# Check validity: Does model || Q |= phi?
	if not models(model, phi, Q, basic_check_name):
		printInvalidInputs(model, phi, Q)
		return 3

	print("Confirmed that model || Q |= phi ...")
	
	# Get the IO.  Is it empty?
	if IO == None:
		return 4

	print("Checked IO is not None ...")
	
	_IO = getIO(IO)
	if _IO == None or len(list(_IO)) == 0:
		printZeroIO(IO)
		return 5

	print("Checked IO is not empty ...")
	
	return _IO

def body(model, phi, Q, IO, max_attacks=1,                  \
	     with_recovery=True, name=None, characterize=False, \
	     cleanUp=False):
	'''
	Body attempts to find attackers against a given model. The attacker 
	is successful if the given phi is violated. The phi is initially 
	evaluated by being composed with Q. 
	@param model        : a promela model 
	@param phi          : LTL property satisfied by model || Q
	@param Q            : a promela model
	@param IO           : Input Output interface of Q's communication channels
	@param max_attacks  : how many attackers to generate
	@param with_recovery: should the attackers be with_recovery?
	@param name         : name of the files
	@param characterize : do you want us to characterize attackers after 
						  producing them?
	@param cleanUp      : do you want us to clean up left-over files at
	                      termination?
	'''
	
	# The name of the file we use to check that model || Q |= phi
	basic_check_name       = name + "_model_Q_phi.pml"
	# The name of the file where we write daisy(Q)
	daisy_name             = name + "_daisy.pml"
	# The name of the file we use to check that (model, (Q), phi) has a 
	# with_recovery attacker
	with_recovery_phi_name = name + "_with_recovery_phi.pml"
	# The subdirectory of out/ where we write our results
	attacker_name          = name + "_" + str(with_recovery)
	# The name of the file we use to check that model || daisy(Q) |/= phi
	daisy_models_name      = name + "_daisy_check.pml" 

	IO = checkArgs(max_attacks, phi, model, Q, basic_check_name, IO)

	distributed = isinstance(IO, list)

	if distributed:
		print("This appears to be a distributed-component attacker TM ...")

	if (not distributed) and (IO in { 1, 2, 3, 4, 5 }):
		_cleanUp(cleanUp)
		return IO

	IO = sorted(list(IO)) # sorted list of events

	daisynames = []
	labels = set()
	if distributed:
		Qs = [f for f in glob(Q + "/*.pml")]
		# Make many daisy attackers
		k = 0
		for io in IO:
			q = Qs[k]
			k += 1
			_daisyname = str(k) + "_" + daisy_name
			net, label = makeDaisy(io,            \
				                   q,             \
				                   with_recovery, \
				                   _daisyname,    \
				                   j=k)
			labels.add(label)
			daisy_string = makeDaisyWithEvents(io, with_recovery, net, label)
			writeDaisyToFile(daisy_string, _daisyname)
			daisynames.append(_daisyname)
	else:
		# Make daisy attacker
		net, label = makeDaisy(IO, Q, with_recovery, daisy_name)
		daisy_string = makeDaisyWithEvents(IO, with_recovery, net, label)
		writeDaisyToFile(daisy_string, daisy_name)

	if with_recovery == False:
		daisyPhi = phi 
	else:
		daisyPhiString = ""
		if distributed:
			daisyPhiString = makeDaisyPhiFinite(labels, phi)
		else:
			daisyPhiString = makeDaisyPhiFinite(label, phi)
		with open(with_recovery_phi_name, "w") as fw:
			fw.write(daisyPhiString)
		daisyPhi = with_recovery_phi_name

	_models = None 
	# ^ to throw an error if neither path evaluates, somehow ...
	if distributed:
		# model, phi, N, name
		_models = models(model, daisyPhi, daisynames, daisy_models_name)
	else:
		_models = models(model, daisyPhi, daisy_name, daisy_models_name)

	if net == None or _models:
		printNoSolution(model, phi, Q, with_recovery)
		_cleanUp(cleanUp)
		return 6

	makeAllTrails(daisy_models_name, max_attacks) 
	# second arg is max# attacks to make

	cmds      			= trailParseCMDs(daisy_models_name)
	attacks, provenance = parseAllTrails(cmds, with_recovery, False, len(daisynames))
	
	# Write these attacks to models
	writeAttacks(attacks, provenance, net, with_recovery, attacker_name, distributed)

	# Characterize the attacks
	if characterize:
		(E, A) = characterizeAttacks(\
			model, phi, with_recovery, attacker_name, distributed)
		_cleanUp(cleanUp)
		return 0 if (E + A) > 0 else -1
	else:
		_cleanUp(cleanUp)
		return 0 # assume it worked if not asked to prove it ...

if __name__== "__main__":
	main()
