ltl phi4 {
	always (
		/* If a peer is in the SYN-RECEIVED state, 
		 * then it will either eventually move to
		 * the ESTABLISHED state, 
		 * the FIN-WAIT-1 state, 
		 * or the CLOSED state. - Ben
		 */
		(state[0] == SynRecState)
			implies (
				eventually (
					(state[0] == EstState   || 
					 state[0] == FinW1State ||
					 state[0] == ClosedState)
				)
			)
		)
}