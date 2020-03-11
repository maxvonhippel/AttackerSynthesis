/* spin -t6 -s -r experiment1_8_False_daisy_check.pml */
active proctype attacker() {
	
	NtoA ! ACK;
	NtoB ! SYN;
	BtoN ? SYN_ACK;
	NtoB ! ACK;
	BtoN ? FIN;
	NtoB ! ACK;
	NtoB ! FIN;
	BtoN ? ACK;
	NtoB ! SYN;
	NtoB ! ACK;
	NtoB ! ACK;
	BtoN ? SYN_ACK;
	// Acceptance Cycle part of attack
}