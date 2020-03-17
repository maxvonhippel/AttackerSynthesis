/* spin -t3 -s -r experiment2_9_False_daisy_check.pml */
active proctype attacker() {
	
	Nto1 ! ACK;
	Nto2 ! ACK;
	2toN ? SYN;
	// Acceptance Cycle part of attack
}