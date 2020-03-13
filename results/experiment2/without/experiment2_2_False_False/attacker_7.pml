/* spin -t7 -s -r experiment2_2_False_daisy_check.pml */
active proctype attacker() {
	
	NtoA ! ACK;
	NtoB ! ACK;
	BtoN ? SYN;
	// Acceptance Cycle part of attack
	do
	::
	   AtoN ? SYN;
	   BtoN ? SYN;
	od
}