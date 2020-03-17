/* spin -t7 -s -r experiment3_6_False_daisy_check.pml */
active proctype attacker() {
	
	Nto1 ! SYN;
	Nto2 ! SYN;
	1toN ? SYN_ACK;
	2toN ? SYN_ACK;
	Nto1 ! FIN;
	Nto2 ! FIN;
	// Acceptance Cycle part of attack
}