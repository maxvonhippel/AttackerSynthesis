active proctype daisy() {
	do
	:: AtoN ? SYN;
	:: AtoN ? FIN;
	:: AtoN ? ACK;
	:: AtoN ? SYN_ACK;
	:: BtoN ? SYN;
	:: BtoN ? FIN;
	:: BtoN ? ACK;
	:: BtoN ? SYN_ACK;
	:: NtoA ! SYN;
	:: NtoA ! FIN;
	:: NtoA ! ACK;
	:: NtoA ! SYN_ACK;
	:: NtoB ! SYN;
	:: NtoB ! FIN;
	:: NtoB ! ACK;
	:: NtoB ! SYN_ACK;
	od
end:
}