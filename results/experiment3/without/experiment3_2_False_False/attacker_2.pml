/* spin -t2 -s -r experiment3_2_False_daisy_check.pml */
active proctype attacker() {
	
	NtoA ! SYN;
	NtoB ! SYN;
	AtoN ? SYN_ACK;
	BtoN ? SYN_ACK;
	NtoA ! FIN;
	NtoB ! FIN;
	// Acceptance Cycle part of attack
}