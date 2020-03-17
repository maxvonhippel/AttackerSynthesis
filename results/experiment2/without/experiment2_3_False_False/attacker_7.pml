/* spin -t7 -s -r experiment2_3_False_daisy_check.pml */
active proctype attacker() {
	
	Nto1 ! ACK;
	Nto2 ! ACK;
	2toN ? SYN;
	// Acceptance Cycle part of attack
	do
	::
	   1toN ? SYN;
	   2toN ? SYN;
	od
}