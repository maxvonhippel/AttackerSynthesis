bool skidding = false;

chan driver2wheel = [0] of { short, short };

active proctype driver() {
	short gas = 3;
	short brake = 0;
	driver2wheel ! gas, brake;
	do
	:: 
		select(gas   : 0..3); 
		select(brake : 0..3); 
		driver2wheel ! gas, brake;
	od
}

active proctype wheel() {
	
	short old_speed, new_speed, g, b;

	driver2wheel ? g, b;
	old_speed = g - b;
	if 
	:: old_speed < 0 -> old_speed = 0;
	:: else -> skip;
	fi

	do
	::
		driver2wheel ? g, b;
		new_speed = old_speed + g - b;
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