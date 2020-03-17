/* spin -t6 -s -r experiment1_4_False_daisy_check.pml */
active proctype attacker() {
	
	Nto1 ! ACK;
	Nto2 ! SYN;
	2toN ? SYN_ACK;
	Nto2 ! ACK;
	2toN ? FIN;
	Nto2 ! ACK;
	Nto2 ! FIN;
	2toN ? ACK;
	Nto2 ! SYN;
	Nto2 ! ACK;
	Nto2 ! ACK;
	2toN ? SYN_ACK;
	// Acceptance Cycle part of attack
}