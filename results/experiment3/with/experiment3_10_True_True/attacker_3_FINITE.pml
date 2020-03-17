/* spin -t3 -s -r experiment3_10_True_daisy_check.pml */
active proctype attacker() {
	
	Nto1 ! SYN;
	Nto2 ! SYN;
	1toN ? SYN_ACK;
	Nto2 ! SYN_ACK;
	2toN ? SYN_ACK;
	Nto1 ! SYN_ACK;
// recovery to N
// N begins here ... 

	do
	:: 1toN ? SYN -> 
		if
		:: Nto2 ! SYN;
		fi unless timeout;
	:: 2toN ? SYN -> 
		if
		:: Nto1 ! SYN;
		fi unless timeout;
	:: 1toN ? FIN -> 
		if
		:: Nto2 ! FIN;
		fi unless timeout;
	:: 2toN ? FIN -> 
		if
		:: Nto1 ! FIN;
		fi unless timeout;
	:: 1toN ? ACK -> 
		if
		:: Nto2 ! ACK;
		fi unless timeout;
	:: 2toN ? ACK -> 
		if
		:: Nto1 ! ACK;
		fi unless timeout;
	:: 1toN ? SYN_ACK -> 
		if
		:: Nto2 ! SYN_ACK;
		fi unless timeout;
	:: 2toN ? SYN_ACK -> 
		if
		:: Nto1 ! SYN_ACK;
		fi unless timeout;
	:: _nr_pr < 3 -> break;
	od
end:

}