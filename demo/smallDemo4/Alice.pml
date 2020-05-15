/* Alice.pml
 * 
 * by Max von Hippel
 * authored 5 May 2020
 *
 */

mtype = { white, royal, pirate, trading }

chan alice2bob = [0] of { mtype }
chan bob2alice = [0] of { mtype }

bool aliceRetired = false

active proctype alice() {
SCOPING:
	if
	:: bob2alice ? _ -> goto PIRATESTUFF;
	fi
PIRATESTUFF:
	alice2bob ! pirate;
	if
	:: bob2alice ? white -> goto SCOPING;
	:: bob2alice ? royal -> goto end;
	fi
end:
	aliceRetired = true
}