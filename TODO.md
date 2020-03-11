# Legend

* `X` means **done**.
* `V` means **experimented with, decided not to do**.  In this case a justification is provided underneath the item.
* `n` means `n` of the things are done where `n` is a number, eg `1`.
* **bold** items are particularly pressing.

# Development TODO List

* `[ ]` Implement message sequence chart generation.
* `[ ]` Implement state machine diagram generation.
* `[ ]` Combine above 2 tasks to make automated report generation.
* `[V]` Change called Spin command to always generate *shortest* attack.
		- *Correct setting is `-i`.  Not worth having because too slow.*
* `[X]` Add logic to error on `max depth too small`.
* `[X]` Add logic to allow manual specification of max depth in the tool, or,
 		to automatically increase the depth until the model checks.
* `[ ]` Figure out a nice way to make it so we *never* get `NOT AN ATTACK` results.
* `[ ]` Come up with a more readable alternative to the `state[i]` notation being used.
* `[ ]` Think about lasso parsing problem.  If we have the lasso `A B (C D)^w` and the lasso
        `A B C (D C)^w`, these are equal.  But it could be that one can be translated into a 
        finite attacker while the other cannot.  We need to figure out the parsing with the
        set `bit b` so that we begin the recovery at the right moment and not just at the moment
        where the lasso occurs!
* `[ ]` Confirm that the above issue is solved in the theory in the paper (Section 5).
* `[X]` I am getting the impression Spin behaves nondeterministically at times, because I get
        non-deterministic test passing in some experiments at times (eg, 
        `tests.test_Gen3.TestGen3.test_works_on_TCP_exp2_not_finite`).  Fix this!
* `[ ]` Figure out how to hide the Spin output from the terminal when running the tool Pythonically.

# Experimental TODO list

* `[ ]` Come up with more properties (say, 5 properties).

# Analytic TODO list

* `[1]` Write written descriptions in the paper of one or more of the discovered
        attacks against TCP.