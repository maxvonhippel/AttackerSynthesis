/* spin -t9 -s -r experiment2_5_False_daisy_check.pml */
active proctype attacker() {
	
	Nto1 ! ACK;
	Nto2 ! ACK;
	2toN ? SYN;
	// Acceptance Cycle part of attack
}