// This is an example attacker I wrote by hand for (P, (Q), phi)
active proctype A() {
	c ! x;
	do
	:: c ! x; c ! y; c ! z;
	od
}