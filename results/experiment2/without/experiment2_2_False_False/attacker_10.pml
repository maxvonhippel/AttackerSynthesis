/* spin -t10 -s -r experiment2_2_False_daisy_check.pml */
active proctype attacker() {
	
	NtoA ! ACK;
	NtoB ! FIN;
	// Acceptance Cycle part of attack
	do
	::
	   BtoN ? SYN;
	od
}