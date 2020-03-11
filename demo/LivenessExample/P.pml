mtype = { x, y, z };
chan c = [0] of { mtype };
bit dead = 0;

active proctype P() {
OFF:
	dead = 0;
	if
	:: c ? x -> goto ON;
	fi
ON:
	dead = 0;
	if
	:: c ? x -> goto OFF;
	:: c ? y -> goto DEAD;
	fi
DEAD:
	dead = 1;
	if
	:: c ? z -> goto OFF;
	fi
}