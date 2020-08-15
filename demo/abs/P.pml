bool skidding = false;

chan flux0 = [0] of { short };
chan flux1 = [0] of { short };
chan flux2 = [0] of { short };

chan sens0 = [0] of { short };
chan sens1 = [0] of { short };
chan sens2 = [0] of { short };

chan driver2wheel = [0] of { short, short };

active proctype driver() {
	short gas   = 3;
	short brake = 0;
	driver2wheel ! gas, brake;
	do
	:: 
		select(gas   : 0..3); 
		select(brake : 0..3); 
		driver2wheel ! gas, brake;
	od
}

chan abs2wheel = [0] of { short };
chan dsp2abs   = [0] of { short };

active proctype abs() {
	short old_speed, new_speed;
	dsp2abs   ? old_speed;
	abs2wheel ! 0;
	do
	::
		dsp2abs ? new_speed;
		if
		:: 
			new_speed - old_speed < -1 -> 
				abs2wheel ! 1; 
				old_speed = new_speed + 1;
		:: 
			else -> 
				abs2wheel ! 0; 
				old_speed = new_speed;
		fi
	od
}

inline send_with_uncertainty(ch, x, e) {
	if
	:: ch ! x;
	:: ch ! x + e;
	:: x - e >= 0 -> ch ! x - e;
	fi
}

inline send_to_sensors(x) {
	send_with_uncertainty(flux0, x, 1);
	send_with_uncertainty(flux1, x, 1);
	send_with_uncertainty(flux2, x, 1);
}

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

active proctype wheel() {
	
	short old_speed, new_speed, g, b, abs_delta;

	driver2wheel ? g, b;
	old_speed = g - b;
	if 
	:: old_speed < 0 -> old_speed = 0;
	:: else -> skip;
	fi
	send_to_sensors(old_speed);

	do
	::
		driver2wheel ? g, b;
		new_speed = old_speed + g - b;
		// ABS
		send_to_sensors(new_speed);
		abs2wheel ? abs_delta;
		if
		:: b > 0 -> new_speed = old_speed + g - b + abs_delta;
		:: else -> skip;
		fi
		// end ABS
		if
		:: new_speed < 0 -> new_speed = 0;
		:: else -> skip;
		fi
		if
		:: new_speed - old_speed < -3 -> skidding = true;
		:: else -> skip;
		fi
		old_speed = new_speed;
	od

}