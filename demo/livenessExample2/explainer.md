# Liveness Example 2

The process `P` is as follows.

````
                        c ? x
                _______________________
               |                       |
               V         c ? x         |
	---> (OFF : {}) --------------> (ON: {})
             ^                         |
             | c ? z                   |
             |                         | c ? y
	    (DEAD : { dead }) <------------/
````

The process `Q` is as follows.

````
                  c ! x
	----> ( q0 ) --------> ( q1 )
	        ^                |
	        |                | c ! y
	        |     c ! z      |
	        \--------------( q2 )
````

The usual behavior of `P || Q` is as follows.

````
             x!               y!                 z!
( OFF, q0 ) ---> ( ON, q1 ) ----> ( DEAD, q2 ) ---->
\________________________ __________________________/
                         V
                         b^omega
````

The property `phi`, which is satisfied by `P || Q`, is

````
ltl alwaysEventuallyDead {
	always ( eventually ( dead == 1 ) )
}
````

What this says is that the system `P` always eventually goes back to `DEAD`.  With recovery, a simple attack exists where you send one `x` over `c` and then recover.  Because of how the composition operator works, no transitions can then be taken.

The property `theta` says:

````
ltl isTrue {
	true
}
````

We just use this for unit-testing, as an example of a property for which no attacker could ever exist.

The property `wrongPhi` says:

````
ltl neverDead {
	!( eventually ( dead == 1 ))
}
````

We use this for unit-testing, as an example of a property not satisfied by `P || Q` to begin with.