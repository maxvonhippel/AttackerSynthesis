/* spin -t9 -s -r experiment2_1_False_daisy_check.pml */
active proctype attacker() {
	
	NtoA ! ACK;
	NtoB ! ACK;
	BtoN ? SYN;
	// Acceptance Cycle part of attack
}