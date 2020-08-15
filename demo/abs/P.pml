bool skidding = false;

/* user brakes      -> speed--
 * user accelerates -> speed++
 * 
 * wheel can only decelerate 2 digits at a time
 * so if deceleration exceeds 2 digits, this means the wheel
 * locks up and the vehicle skids in the next time step.
 */

chan sens0 = [0] of { short };
chan sens1 = [0] of { short };
chan sens2 = [0] of { short };

chan flux0 = [0] of { short };
chan flux1 = [0] of { short };
chan flux2 = [0] of { short };

active proctype wheel() {
	short wheel_speed = 0;
	short vehicle_speed = 0;
	short gas_p, brake_p, abs_d, tmp, acc;
LOOP:
	// non-deterministically select gas amount.
	select(gas_p : 1..4);
	// non-deterministically select brake amount.
	select(brake_p : 1..4);
	// calculate new wheel speed.
	tmp = wheel_speed + gas_p - brake_p;
	if
	:: tmp < 0 -> tmp = 0;
	:: else -> skip;
	fi
	// calculate acceleration
	acc = tmp - wheel_speed;
	// check if skidding
	if 
	:: tmp < -2 -> skidding = true;
	:: else -> skip
	fi
	// loop again
	goto LOOP;
}