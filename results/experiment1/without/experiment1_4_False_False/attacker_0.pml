/* spin -t0 -s -r experiment1_4_False_daisy_check.pml */
active proctype attacker() {
	
	Nto1 ! ACK;
	Nto2 ! SYN;
	2toN ? SYN_ACK;
	Nto2 ! ACK;
	// Acceptance Cycle part of attack
}