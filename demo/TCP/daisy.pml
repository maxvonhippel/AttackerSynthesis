active proctype daisy() {
	do
	:: 1toN ? SYN;
	:: 1toN ? ACK;
	:: 1toN ? SYN_ACK;
	:: 1toN ? FIN;
	:: 2toN ? SYN;
	:: 2toN ? ACK;
	:: 2toN ? SYN_ACK;
	:: 2toN ? FIN;
	:: Nto1 ! SYN;
	:: Nto1 ! ACK;
	:: Nto1 ! SYN_ACK;
	:: Nto1 ! FIN;
	:: Nto2 ! SYN;
	:: Nto2 ! ACK;
	:: Nto2 ! SYN_ACK;
	:: Nto2 ! FIN;
	od
}