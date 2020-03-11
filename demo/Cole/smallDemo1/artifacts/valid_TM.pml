/*                                                ___
 *                             ________________      |
 *                 A!         |                |     |
 * -->( P_0 { 1 } )------>( P_1 { 0 } )<-------|     |
 *        ^                   ^            C?        |> P
 *        |___________________|                      |
 *                  B!                               |
 *                                                ___|
 *
 *
 *               C!, A?                           ___
 * -->( Q_0   )----------->( Q_1  )--|               |
 *        ^                          |               |
 *        |__________________________|               |> Q
 *                 B?, C!                            |
 *                                                ___|
 *
 *              phi := G F ~ w
 *
 */

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

active proctype Q() {
QZERO:
	if
	:: channel ! C; goto QONE;
	:: channel ? A; goto QONE;
	fi
QONE:
	if 
	:: channel ? B; goto QZERO;
	:: channel ! C; goto QZERO;
	fi
}

ltl alwaysEventuallyW {
	always eventually (w == 0)
}