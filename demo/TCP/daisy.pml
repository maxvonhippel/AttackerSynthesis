active proctype daisy() {
	do
	:: AtoN ? SYN;
	:: AtoN ? ACK;
	:: AtoN ? SYN_ACK;
	:: AtoN ? FIN;
	:: BtoN ? SYN;
	:: BtoN ? ACK;
	:: BtoN ? SYN_ACK;
	:: BtoN ? FIN;
	:: NtoA ! SYN;
	:: NtoA ! ACK;
	:: NtoA ! SYN_ACK;
	:: NtoA ! FIN;
	:: NtoB ! SYN;
	:: NtoB ! ACK;
	:: NtoB ! SYN_ACK;
	:: NtoB ! FIN;
	od
}