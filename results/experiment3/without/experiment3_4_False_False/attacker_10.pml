/* spin -t10 -s -r experiment3_4_False_daisy_check.pml */
active proctype attacker() {
	
	NtoA ! SYN;
	NtoB ! SYN;
	AtoN ? SYN_ACK;
	BtoN ? SYN_ACK;
	NtoA ! SYN;
	NtoB ! FIN;
	// Acceptance Cycle part of attack
}