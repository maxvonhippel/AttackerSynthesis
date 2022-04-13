active proctype daisy() {
	do
	:: AtoN ? SYN;
	:: AtoN ? ACK;
	:: AtoN ? FIN;
	:: BtoN ? SYN;
	:: BtoN ? ACK;
	:: BtoN ? FIN;
	:: NtoA ! SYN;
	:: NtoA ! ACK;
	:: NtoA ! FIN;
	:: NtoB ! SYN;
	:: NtoB ! ACK;
	:: NtoB ! FIN;
	od
}