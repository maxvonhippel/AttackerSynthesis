/* spin -t4 -s -r experiment3_1_False_daisy_check.pml */
active proctype attacker() {
	
	Nto1 ! SYN;
	Nto2 ! SYN;
	1toN ? SYN_ACK;
	2toN ? SYN_ACK;
	Nto1 ! FIN;
	Nto2 ! SYN;
	// Acceptance Cycle part of attack
}