int state[2];
int pids[2];

#define ClosedState    0
#define ListenState    1
#define SynSentState   2
#define SynRecState    3
#define EstState       4
#define FinW1State     5
#define CloseWaitState 6
#define FinW2State     7
#define ClosingState   8
#define LastAckState   9
#define TimeWaitState  10
#define EndState       -1

#define leftConnecting (state[0] == ListenState && state[1] == SynSentState)
#define leftEstablished (state[0] == EstState)
#define rightEstablished (state[1] == EstState)
#define leftClosed (state[0] == ClosedState)
mtype = { SYN, ACK, FIN }
chan AtoN = [1] of { mtype }
chan NtoA = [0] of { mtype }
chan BtoN = [1] of { mtype }
chan NtoB = [0] of { mtype }

active proctype peerA(){
	goto LISTEN;
CLOSED:
	state[0] = ClosedState;
	if
	:: AtoN ! FIN; goto ESTABLISHED;
	fi
CLOSE_WAIT:
	state[0] = CloseWaitState;
	if
	:: AtoN ! FIN; goto CLOSING;
	:: NtoA ? FIN; AtoN ! ACK; goto CLOSE_WAIT;
	fi
CLOSING:
	state[0] = ClosingState;
	if
	:: NtoA ? FIN; AtoN ! ACK; goto CLOSING;
	fi
ESTABLISHED:
	state[0] = EstState;
	if
	:: AtoN ! FIN; goto FIN_WAIT_1;
	:: NtoA ? FIN; AtoN ! ACK; goto CLOSE_WAIT;
	:: NtoA ? FIN; AtoN ! ACK; goto TIME_WAIT;
	:: NtoA ? FIN; AtoN ! ACK; goto CLOSING;
	fi
FIN_WAIT_1:
	state[0] = FinW1State;
	if
	:: skip;
	fi
FIN_WAIT_2:
	state[0] = FinW2State;
	if
	:: NtoA ? FIN; AtoN ! ACK; goto TIME_WAIT;
	fi
LAST_ACK:
	state[0] = LastAckState;
	if
	:: NtoA ? FIN; goto CLOSING;
	:: NtoA ? FIN; goto CLOSED;
	:: NtoA ? FIN; AtoN ! ACK; goto LAST_ACK;
	fi
LISTEN:
	state[0] = ListenState;
	if
	:: AtoN ! SYN; goto SYN_SENT;
	:: NtoA ? FIN; goto ESTABLISHED;
	:: NtoA ? ACK; goto SYN_RECEIVED;
	fi
SYN_RECEIVED:
	state[0] = SynRecState;
	if
	:: AtoN ! SYN; goto ESTABLISHED;
	:: NtoA ? FIN; goto ESTABLISHED;
	:: NtoA ? FIN; AtoN ! ACK; goto CLOSE_WAIT;
	:: NtoA ? FIN; AtoN ! ACK; goto TIME_WAIT;
	:: NtoA ? FIN; AtoN ! ACK; goto CLOSING;
	fi
SYN_SENT:
	state[0] = SynSentState;
	if
	:: AtoN ! SYN; goto ESTABLISHED;
	:: NtoA ? FIN; goto ESTABLISHED;
	:: AtoN ! ACK; AtoN ! SYN; goto ESTABLISHED;
	:: AtoN ! ACK; AtoN ! SYN; goto SYN_RECEIVED;
	:: NtoA ? ACK; goto ESTABLISHED;
	fi
TIME_WAIT:
	state[0] = TimeWaitState;
	if
	:: NtoA ? FIN; goto CLOSING;
	:: NtoA ? FIN; AtoN ! ACK; goto TIME_WAIT;
	fi
}
active proctype peerB(){
	goto LISTEN;
CLOSED:
	state[1] = ClosedState;
	if
	:: BtoN ! FIN; goto ESTABLISHED;
	fi
CLOSE_WAIT:
	state[1] = CloseWaitState;
	if
	:: BtoN ! FIN; goto CLOSING;
	:: NtoB ? FIN; BtoN ! ACK; goto CLOSE_WAIT;
	fi
CLOSING:
	state[1] = ClosingState;
	if
	:: NtoB ? FIN; BtoN ! ACK; goto CLOSING;
	fi
ESTABLISHED:
	state[1] = EstState;
	if
	:: BtoN ! FIN; goto FIN_WAIT_1;
	:: NtoB ? FIN; BtoN ! ACK; goto CLOSE_WAIT;
	:: NtoB ? FIN; BtoN ! ACK; goto TIME_WAIT;
	:: NtoB ? FIN; BtoN ! ACK; goto CLOSING;
	fi
FIN_WAIT_1:
	state[1] = FinW1State;
	if
	:: skip;
	fi
FIN_WAIT_2:
	state[1] = FinW2State;
	if
	:: NtoB ? FIN; BtoN ! ACK; goto TIME_WAIT;
	fi
LAST_ACK:
	state[1] = LastAckState;
	if
	:: NtoB ? FIN; goto CLOSING;
	:: NtoB ? FIN; goto CLOSED;
	:: NtoB ? FIN; BtoN ! ACK; goto LAST_ACK;
	fi
LISTEN:
	state[1] = ListenState;
	if
	:: BtoN ! SYN; goto SYN_SENT;
	:: NtoB ? FIN; goto ESTABLISHED;
	:: NtoB ? ACK; goto SYN_RECEIVED;
	fi
SYN_RECEIVED:
	state[1] = SynRecState;
	if
	:: BtoN ! SYN; goto ESTABLISHED;
	:: NtoB ? FIN; goto ESTABLISHED;
	:: NtoB ? FIN; BtoN ! ACK; goto CLOSE_WAIT;
	:: NtoB ? FIN; BtoN ! ACK; goto TIME_WAIT;
	:: NtoB ? FIN; BtoN ! ACK; goto CLOSING;
	fi
SYN_SENT:
	state[1] = SynSentState;
	if
	:: BtoN ! SYN; goto ESTABLISHED;
	:: NtoB ? FIN; goto ESTABLISHED;
	:: BtoN ! ACK; BtoN ! SYN; goto ESTABLISHED;
	:: BtoN ! ACK; BtoN ! SYN; goto SYN_RECEIVED;
	:: NtoB ? ACK; goto ESTABLISHED;
	fi
TIME_WAIT:
	state[1] = TimeWaitState;
	if
	:: NtoB ? FIN; goto CLOSING;
	:: NtoB ? FIN; BtoN ! ACK; goto TIME_WAIT;
	fi
}

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

	printf("Recovery") 

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

// spin -run -a -DNOREDUCE -e -c99 daisy.P.phi.pml
// spin -t68 -s -r -g daisy.P.phi.pml