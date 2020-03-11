'''
							Generator3.py
				Authored 30 November 2019 by Max von Hippel
USAGE:
	
	See the Makefile, as this often changes at the moment.

WHERE:

	TODO: Write this once the interface is locked down & no longer
	actively evolving.

RETURNS:

	A (M, (Q), phi)-attacker, optionally with recovery to Q.

NOTE:

	This code is not even remotely cyber-secure and should only be
	run locally on inputs you personally manufactured.  Otherwise you expose
	yourself to a basically trivial remote code execution issue in Bash,
	because of the way I am hacking on subprocess.

'''
from CLI          import *
from Characterize import *
from Construct    import *

@cleanUp
def main():
	args = getArgs()
	model, phi, Q, IO, max_attacks, finite, name, characterize = \
		args.model, 	             \
		args.phi, 		             \
		args.Q, 		             \
		args.IO,                     \
		args.max_attacks,            \
		args.finite,                 \
		args.name,                   \
		args.characterize
	return body(model, phi, Q, IO, max_attacks, finite, False, name, characterize)

def checkArgs(max_attacks, TESTING, phi, model, Q, basic_check_name, IO):
	if max_attacks == None or max_attacks < 1:
		printInvalidNum(max_attacks, TESTING)
		return 1

	# Can we negate phi?  This is important.
	if not negateClaim(phi):
		printCouldNotNegateClaim(phi, TESTING)
		return 2
	
	# Check validity: Does model || Q |= phi?
	if not models(model, phi, Q, basic_check_name):
		printInvalidInputs(model, phi, Q, TESTING)
		return 3
	
	# Get the IO.  Is it empty?
	if IO == None:
		if not TESTING:
			print("No IO.")
		return 4
	
	_IO = getIO(IO)
	if _IO == None or len(list(_IO)) == 0:
		printZeroIO(IO, TESTING)
		return 5
	
	return _IO

def body(model, phi, Q, IO, max_attacks=1, finite=True, TESTING=False, name=None, characterize=False):
	'''
	Body attempts to find attackers against a given model. The attacker 
	is successful if the given phi is violated. The phi is initially 
	evaluated by being composed with Q. 
	@param model        : a promela model 
	@param phi          : LTL property satisfied by model || Q
	@param Q            : a promela model
	@param IO           : Input Output interface of Q's communication channels
	@param max_attacks  : how many attackers to generate
	@param finite       : should the attackers be finite?
	@param TESTING      : are you testing? 
	@param name         : name of the files
	@param characterize : do you want us to characterize attackers after producing them?
	'''
	assert(name != None)
	
	# The name of the file we use to check that model || Q |= phi
	basic_check_name  = name + "_model_Q_phi.pml"
	# The name of the file where we write daisy(Q)
	daisy_name        = name + "_daisy.pml"
	# The name of the file we use to check that (model, (Q), phi) has a finite attacker
	finite_phi_name   = name + "_finite_phi.pml"
	# The subdirectory of out/ where we write our results
	attacker_name     = name + "_" + str(finite)
	# The name of the file we use to check that model || daisy(Q) |/= phi
	daisy_models_name = name + "_daisy_check.pml" 

	IO = checkArgs(max_attacks, TESTING, phi, model, Q, basic_check_name, IO)
	if IO in { 1, 2, 3, 4, 5 }:
		return IO
	IO = sorted(list(IO)) # sorted list of events
	# Make daisy attacker
	net, label = makeDaisy(IO, Q, finite, daisy_name)
	daisy_string = makeDaisyWithEvents(IO, finite, net, label)
	writeDaisyToFile(daisy_string, daisy_name)

	
	if finite == False:
		daisyPhi = phi 
	else:
		daisyPhiString = makeDaisyPhiFinite(label, phi)
		with open(finite_phi_name, "w") as fw:
			fw.write(daisyPhiString)
		daisyPhi = finite_phi_name
			
	# model, phi, N, name
	_models = models(model, daisyPhi, daisy_name, daisy_models_name)
		
	if net == None or _models:
		printNoSolution(model, phi, Q, finite, TESTING)
		return 6
	
	makeAllTrails(daisy_models_name, max_attacks) 
	# second arg is max# attacks to make

	cmds      			= trailParseCMDs(daisy_models_name)
	attacks, provenance = parseAllTrails(cmds, finite)
	
	# Write these attacks to models
	writeAttacks(attacks, provenance, net, finite, attacker_name)
	
	# Delete the trail files
	cleanUpTargeted("*.trail")
	
	# Characterize the attacks
	if characterize:
		(E, A) = characterizeAttacks(model, phi, finite, attacker_name)
		return 0 if (E + A) > 0 else -1
	else:
		return 0 # assume it worked if not asked to prove it ...

if __name__== "__main__":
	main()