/* spin -t10 -s -r experiment1_10_False_daisy_check.pml */
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
	NtoB ! FIN;
	NtoB ! SYN;
	BtoN ? FIN;
	BtoN ? ACK;
	BtoN ? SYN;
	NtoB ! ACK;
	NtoB ! FIN;
	// Acceptance Cycle part of attack
}