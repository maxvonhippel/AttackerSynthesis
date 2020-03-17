/* spin -t10 -s -r experiment2_1_False_daisy_check.pml */
active proctype attacker() {
	
	Nto1 ! ACK;
	Nto2 ! FIN;
	// Acceptance Cycle part of attack
	do
	::
	   2toN ? SYN;
	od
}