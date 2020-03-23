mtype = { A, B };

chan channel = [0] of { mtype };

bit w = 1;

active proctype P() {
PZERO:
	w = 1;
	if 
	:: channel ! A; goto PZERO;
	:: channel ! B; goto PONE;
	fi
PONE:
	w = 0;
	if 
	:: channel ! B; goto PONE;
	fi
}