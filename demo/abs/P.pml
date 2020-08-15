chan flux0 = [1] of { short };
chan flux1 = [1] of { short };
chan flux2 = [1] of { short };

chan sens0 = [1] of { short };
chan sens1 = [1] of { short };
chan sens2 = [1] of { short };

typedef vehicle_inputs {
	short gas;
	short brake;
	short abs_delta;
}

typedef vehicle_dynamics {
	short vehicle_speed;
	short wheel_speed;
}

bool skidding = false;

chan dsp2abs = [0] of { short };

active proctype DSP() {
	short x, y, z;
	do
	::
		sens0 ? x;
		sens1 ? y;
		sens2 ? z;
		dsp2abs ! (x + y + z) / 3;
	od
}

mtype { MAINTAIN_BRAKE, DECREASE_BRAKE }

chan abs2vehicle = [0] of { mtype };

active proctype ABS() {
	short prior_wheel_speed = 0;
	short cur_wheel_speed;
	short apparent_acceleration;
	do
	::
		dsp2abs ? cur_wheel_speed;
		apparent_acceleration = cur_wheel_speed - prior_wheel_speed;
		if
		:: apparent_acceleration < -2 -> abs2vehicle ! DECREASE_BRAKE;
		:: else                       -> abs2vehicle ! MAINTAIN_BRAKE;
		fi
		prior_wheel_speed = cur_wheel_speed;
	od
}

inline broadcast_with_uncertainty(ch, x, u) {
	if
	:: ch ! x;
	:: ch ! x + u;
	:: ch ! x - u;
	fi
}

active proctype vehicle() {
	vehicle_inputs   cur_inputs;
	vehicle_dynamics prior_dynamics;
	vehicle_dynamics cur_dynamics;
	mtype abs_command;
	short tmp, new_wheel_speed, new_vehicle_speed;
	do
	::
		/* non-deterministically decide gas */
		select(tmp : 1..4);
		cur_inputs.gas = tmp;
		/* non-deterministically decide brake */
		select(tmp : 1..4);
		cur_inputs.brake = tmp;
		/* listen to ABS for instruction */
		if
		:: abs2vehicle ? DECREASE_BRAKE -> cur_inputs.abs_delta = 1;
		:: abs2vehicle ? MAINTAIN_BRAKE -> cur_inputs.abs_delta = 0;
		fi
		/* decide new amount of brake */
		tmp = cur_inputs.brake - cur_inputs.abs_delta;
		if
		:: tmp < 0 -> tmp = 0; /* cannot brake so hard we go backward */
		:: else -> skip; /* otherwise we are fine */
		fi 
		/* apply current modulated inputs to vehicle dynamics */
		new_wheel_speed = prior_dynamics.wheel_speed + cur_inputs.gas - tmp;
		if
		:: new_wheel_speed < 0 -> new_wheel_speed = 0;
		:: else -> skip;
		fi
		if
		:: 
			new_wheel_speed - prior_dynamics.wheel_speed < -2 -> 
				/* we are skiddng */
				new_vehicle_speed = prior_dynamics.vehicle_speed;
				skidding = true;
		:: 
			else -> new_vehicle_speed = new_wheel_speed; skidding = false;
		fi
		/* finally, tone-wheel broadcasts dynamics to the sensors */
		broadcast_with_uncertainty(flux0, new_wheel_speed, 1);
		broadcast_with_uncertainty(flux1, new_wheel_speed, 1);
		broadcast_with_uncertainty(flux2, new_wheel_speed, 1);
		/* and update */
		prior_dynamics.wheel_speed = cur_dynamics.wheel_speed;
		prior_dynamics.vehicle_speed = cur_dynamics.vehicle_speed;
	od
}