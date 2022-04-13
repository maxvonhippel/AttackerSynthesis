ltl phi4 {
	always (
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