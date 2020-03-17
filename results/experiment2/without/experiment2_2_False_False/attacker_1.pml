/* spin -t1 -s -r experiment2_2_False_daisy_check.pml */
active proctype attacker() {
	
	Nto1 ! ACK;
	Nto2 ! ACK;
	// Acceptance Cycle part of attack
	do
	::
	   2toN ? SYN;
	od
}