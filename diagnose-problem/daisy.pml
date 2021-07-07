bit b= 0;
active proctype daisy () {
	do
	:: AtoN?ACK;
	:: AtoN?FIN;
	:: AtoN?SYN;
	:: BtoN?ACK;
	:: BtoN?FIN;
	:: BtoN?SYN;
	:: NtoA!ACK;
	:: NtoA!FIN;
	:: NtoA!SYN;
	:: NtoB!ACK;
	:: NtoB!FIN;
	:: NtoB!SYN;
	:: break; // recovery to N ... 
	od
	b = 1;
	// N begins here ... 

	do
	:: AtoN ? SYN -> NtoB ! SYN;
	:: AtoN ? ACK -> NtoB ! ACK;
	:: AtoN ? FIN -> NtoB ! FIN;
	:: BtoN ? SYN -> NtoA ! SYN;
	:: BtoN ? ACK -> NtoA ! ACK;
	:: BtoN ? FIN -> NtoA ! FIN;
	od

}
ltl newPhi {
	(eventually ( b == 1 ) ) implies (
		
	always (
		/* If a peer is in the SYN-RECEIVED state, 
		 * then it will either eventually move to
		 * the ESTABLISHED state, 
		 * the FIN-WAIT-1 state, 
		 * or the CLOSED state. - Ben
		 *
		 * STATUS: SATISFIES CANONICAL-TCP-TEST.
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
  )
}
