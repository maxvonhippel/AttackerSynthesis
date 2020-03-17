/* spin -t5 -s -r experiment3_5_False_daisy_check.pml */
active proctype attacker() {
	
	Nto1 ! SYN;
	Nto2 ! SYN;
	1toN ? SYN_ACK;
	2toN ? SYN_ACK;
	Nto1 ! FIN;
	Nto2 ! SYN_ACK;
	// Acceptance Cycle part of attack
}