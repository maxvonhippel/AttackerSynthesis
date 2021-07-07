/* spin -t68 -s -r attack-promela-models.TCP.props.phi5-TCP-_daisy_check.pml */
active proctype attacker() {
	
	NtoB ! ACK;
	NtoB ! FIN;
	NtoB ! FIN;
	BtoN ? ACK;
	NtoB ! FIN;
	BtoN ? ACK;
	NtoA ! ACK;
	NtoB ! FIN;
	NtoB ! FIN;
// recovery to N
// N begins here ... 

	do
	:: AtoN ? SYN -> NtoB ! SYN;
	:: AtoN ? ACK -> NtoB ! ACK;
	:: AtoN ? FIN -> NtoB ! FIN;
	:: BtoN ? SYN -> NtoA ! SYN;
	:: BtoN ? ACK -> NtoA ! ACK;
	:: BtoN ? FIN -> NtoA ! FIN;
	od

}