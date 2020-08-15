
active proctype sensor0() {
	short x;
	do
	:: flux0 ? x -> sens0 ! x;
	od
}