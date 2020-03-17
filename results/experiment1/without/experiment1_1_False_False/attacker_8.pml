/* spin -t8 -s -r experiment1_1_False_daisy_check.pml */
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
	Nto2 ! FIN;
	Nto2 ! SYN;
	2toN ? FIN;
	2toN ? ACK;
	2toN ? SYN;
	Nto2 ! ACK;
	Nto2 ! ACK;
	// Acceptance Cycle part of attack
}