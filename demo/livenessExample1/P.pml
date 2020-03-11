mtype = { A, B, C };

chan channel = [0] of { mtype };

bit w = 0;

active proctype P() {
PZERO:
	w = 1;
	channel ! A; goto PONE; 
PONE:
	w = 0;
	if 
	:: channel ! B; goto PZERO;
	:: channel ? C; goto PONE;
	fi
}