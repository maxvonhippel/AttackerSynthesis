/* spin -t3 -s -r experiment2_6_False_daisy_check.pml */
active proctype attacker() {
	
	NtoA ! ACK;
	NtoB ! ACK;
	BtoN ? SYN;
	// Acceptance Cycle part of attack
}