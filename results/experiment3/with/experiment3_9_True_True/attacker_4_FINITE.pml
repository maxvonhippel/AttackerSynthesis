/* spin -t4 -s -r experiment3_9_True_daisy_check.pml */
active proctype attacker() {
	
	NtoA ! SYN;
	NtoB ! SYN;
	BtoN ? SYN_ACK;
	NtoA ! SYN_ACK;
	AtoN ? SYN_ACK;
	NtoB ! SYN_ACK;
// recovery to N
// N begins here ... 

	do
	:: AtoN ? SYN -> 
		if
		:: NtoB ! SYN;
		fi unless timeout;
	:: BtoN ? SYN -> 
		if
		:: NtoA ! SYN;
		fi unless timeout;
	:: AtoN ? FIN -> 
		if
		:: NtoB ! FIN;
		fi unless timeout;
	:: BtoN ? FIN -> 
		if
		:: NtoA ! FIN;
		fi unless timeout;
	:: AtoN ? ACK -> 
		if
		:: NtoB ! ACK;
		fi unless timeout;
	:: BtoN ? ACK -> 
		if
		:: NtoA ! ACK;
		fi unless timeout;
	:: AtoN ? SYN_ACK -> 
		if
		:: NtoB ! SYN_ACK;
		fi unless timeout;
	:: BtoN ? SYN_ACK -> 
		if
		:: NtoA ! SYN_ACK;
		fi unless timeout;
	:: _nr_pr < 3 -> break;
	od
end:

}