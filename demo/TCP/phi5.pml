ltl phi5 {
	always (
		/* A peer in the CLOSING state will 
		 * next go into the CLOSED state - Ben
		 */
		(state[0] == ClosingState)
			implies
				(next (state[0] == ClosingState ||
					   state[0] == ClosedState))
	)
}