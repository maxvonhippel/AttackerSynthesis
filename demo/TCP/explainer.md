# `phi1.pml`

The property is

````
ltl exp1 {
	always ( leftClosed implies !rightEstablished )
}
````
What this property says is that if Peer 1 is in Closed, then, Peer 2 cannot be in Established.  A violation of this property would constitute a half-open connection, which is bad (as explained in the RFC).

# `phi2.pml`

The property is
````
ltl exp2 {
	( (always ( eventually ( state[0] == 1 && state[1] == 2 ) ) ) 
		implies ( eventually ( state[0] == 4 ) ) )
}

````
What this property says is that if it is infinitely often true that the peers attempt an active/passive connection establishment routine, then it is eventually true that one of the peers establishes a connection.  (Note that if this holds and `phi1.pml` holds then they must both be connected, assuming basic model symmetry, which is reasonable.)

# `phi3.pml`

The property is
````
ltl exp3 {
  !(eventually (((always (state[0] == SynSentState))   ||
                 (always (state[0] == SynRecState))    ||
                 (always (state[0] == EstState))       ||
                 (always (state[0] == FinW1State))     ||
                 (always (state[0] == CloseWaitState)) ||
                 (always (state[0] == FinW2State))     ||
                 (always (state[0] == ClosingState))   ||
                 (always (state[0] == LastAckState))   ||
                 (always (state[0] == TimeWaitState)))
                &&
                ((always (state[1] == SynSentState))   ||
                 (always (state[1] == SynRecState))    ||
                 (always (state[1] == EstState))       ||
                 (always (state[1] == FinW1State))     ||
                 (always (state[1] == CloseWaitState)) ||
                 (always (state[1] == FinW2State))     ||
                 (always (state[1] == ClosingState))   ||
                 (always (state[1] == LastAckState))   ||
                 (always (state[1] == TimeWaitState)))))
}
````
What this says is that the only place (Peer 1, Peer 2) can "stay still" forever (either deadlocking or self-looping) is in an element of `{ Closed, End } x { Closed, End }`.  This property can capture DOS attack scenarios, and non-progress.

Actually, just using Spin's built-in non-progress cycle checking is easier, but we wrote the property this way so that it could be explained in the paper without having to rely on Spin's backend machinery.