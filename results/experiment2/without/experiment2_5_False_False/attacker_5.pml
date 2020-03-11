/* spin -t5 -s -r experiment2_5_False_daisy_check.pml */
active proctype attacker() {
	
	NtoA ! ACK;
	NtoB ! ACK;
	BtoN ? SYN;
	// Acceptance Cycle part of attack
}