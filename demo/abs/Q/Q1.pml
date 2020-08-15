
active proctype sensor1() {
	short x;
	do
	:: flux1 ? x -> sens1 ! x;
	od
}