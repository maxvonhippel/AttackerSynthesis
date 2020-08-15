bool skidding = false;

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

chan wheel2abs = [0] of { short };
chan abs2wheel = [0] of { short };

active proctype abs() {
	short old_speed, new_speed;
	wheel2abs ? old_speed;
	abs2wheel ! 0;
	do
	::
		wheel2abs ? new_speed;
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

active proctype wheel() {
	
	short old_speed, new_speed, g, b, abs_delta;

	driver2wheel ? g, b;
	old_speed = g - b;
	if 
	:: old_speed < 0 -> old_speed = 0;
	:: else -> skip;
	fi
	wheel2abs ! old_speed;

	do
	::
		driver2wheel ? g, b;
		new_speed = old_speed + g - b;
		// ABS
		wheel2abs ! new_speed;
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
		:: new_speed - old_speed < -2 -> skidding = true;
		:: else -> skip;
		fi
		old_speed = new_speed;
	od

}

ltl no_skid { 
	always ( skidding == false )
}