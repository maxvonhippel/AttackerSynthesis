/* spin -t2 -s -r experiment1_3_False_daisy_check.pml */
active proctype attacker() {
	
	NtoA ! ACK;
	NtoB ! SYN;
	BtoN ? SYN_ACK;
	NtoB ! ACK;
	// Acceptance Cycle part of attack
}