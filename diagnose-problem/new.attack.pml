active proctype attacker() {
    // 4: proc  2 (daisy:1) daisy.P.phi.pml:190 Sent ACK  -> queue 1 (NtoB)
    NtoB ! ACK;
    //   5: proc  1 (peerB:1) daisy.P.phi.pml:150 Recv ACK  <- queue 1 (NtoB)
    //   9: proc  2 (daisy:1) daisy.P.phi.pml:191 Sent FIN  -> queue 1 (NtoB)
    NtoB ! FIN;
    //  10: proc  1 (peerB:1) daisy.P.phi.pml:156 Recv FIN  <- queue 1 (NtoB)
    //  14: proc  2 (daisy:1) daisy.P.phi.pml:191 Sent FIN  -> queue 1 (NtoB)
    NtoB ! FIN;
    //  15: proc  1 (peerB:1) daisy.P.phi.pml:124 Recv FIN  <- queue 1 (NtoB)
    //  17: proc  1 (peerB:1) daisy.P.phi.pml:124 Send ACK  -> queue 2 (BtoN)
    //  19: proc  2 (daisy:1) daisy.P.phi.pml:184 Recv ACK  <- queue 2 (BtoN)
    BtoN ? ACK;
    //  23: proc  2 (daisy:1) daisy.P.phi.pml:191 Sent FIN  -> queue 1 (NtoB)
    NtoB ! FIN;
    //  24:    proc  1 (peerB:1) daisy.P.phi.pml:113 Recv FIN  <- queue 1 (NtoB)
    //  26:    proc  1 (peerB:1) daisy.P.phi.pml:113 Send ACK  -> queue 2 (BtoN)
    //  28:    proc  2 (daisy:1) daisy.P.phi.pml:184 Recv ACK  <- queue 2 (BtoN)
    BtoN ? ACK;
    //  32: proc  2 (daisy:1) daisy.P.phi.pml:187 Sent ACK  -> queue 3 (NtoA)
    NtoA ! ACK;
    //  33: proc  0 (peerA:1) daisy.P.phi.pml:75 Recv ACK   <- queue 3 (NtoA)
    //  37: proc  2 (daisy:1) daisy.P.phi.pml:191 Sent FIN  -> queue 1 (NtoB)
    NtoB ! FIN;
    //  38: proc  1 (peerB:1) daisy.P.phi.pml:113 Recv FIN  <- queue 1 (NtoB)
    //  40: proc  1 (peerB:1) daisy.P.phi.pml:113 Send ACK  -> queue 2 (BtoN)
    //  44: proc  2 (daisy:1) daisy.P.phi.pml:191 Sent FIN  -> queue 1 (NtoB)
    NtoB ! FIN;
    //  45: proc  1 (peerB:1) daisy.P.phi.pml:113 Recv FIN  <- queue 1 (NtoB)
    b = 1;
    do
    :: AtoN ? SYN -> NtoB ! SYN;
    :: AtoN ? ACK -> NtoB ! ACK;
    :: AtoN ? FIN -> NtoB ! FIN;
    :: BtoN ? SYN -> NtoA ! SYN;
    :: BtoN ? ACK -> NtoA ! ACK;
    :: BtoN ? FIN -> NtoA ! FIN;
    od
}

/*
      <<<<<START OF CYCLE>>>>>
Never claim moves to line 4	[((!(!((state[0]==3)))&&!((((state[0]==4)||(state[0]==5))||(state[0]==0)))))]
 49:	proc  2 (daisy:1) daisy.P.phi.pml:184 Recv ACK	<- queue 2 (BtoN)
Never claim moves to line 15	[(!((((state[0]==4)||(state[0]==5))||(state[0]==0))))]
 51:	proc  2 (daisy:1) daisy.P.phi.pml:188 Sent FIN	-> queue 3 (NtoA)
 52:	proc  0 (peerA:1) daisy.P.phi.pml:82 Recv FIN	<- queue 3 (NtoA)
 54:	proc  1 (peerB:1) daisy.P.phi.pml:113 Send ACK	-> queue 2 (BtoN)
 56:	proc  2 (daisy:1) daisy.P.phi.pml:184 Recv ACK	<- queue 2 (BtoN)
 60:	proc  1 (peerB:1) daisy.P.phi.pml:112 Send FIN	-> queue 2 (BtoN)
 62:	proc  2 (daisy:1) daisy.P.phi.pml:185 Recv FIN	<- queue 2 (BtoN)
 66:	proc  2 (daisy:1) daisy.P.phi.pml:191 Sent FIN	-> queue 1 (NtoB)
 67:	proc  1 (peerB:1) daisy.P.phi.pml:118 Recv FIN	<- queue 1 (NtoB)
 69:	proc  1 (peerB:1) daisy.P.phi.pml:118 Send ACK	-> queue 2 (BtoN)
 71:	proc  2 (daisy:1) daisy.P.phi.pml:184 Recv ACK	<- queue 2 (BtoN)
 73:	proc  0 (peerA:1) daisy.P.phi.pml:82 Send ACK	-> queue 4 (AtoN)
 75:	proc  2 (daisy:1) daisy.P.phi.pml:181 Recv ACK	<- queue 4 (AtoN)
 79:	proc  2 (daisy:1) daisy.P.phi.pml:191 Sent FIN	-> queue 1 (NtoB)
 80:	proc  1 (peerB:1) daisy.P.phi.pml:118 Recv FIN	<- queue 1 (NtoB)
 82:	proc  1 (peerB:1) daisy.P.phi.pml:118 Send ACK	-> queue 2 (BtoN)
 86:	proc  2 (daisy:1) daisy.P.phi.pml:191 Sent FIN	-> queue 1 (NtoB)
 87:	proc  1 (peerB:1) daisy.P.phi.pml:118 Recv FIN	<- queue 1 (NtoB)
 91:	proc  2 (daisy:1) daisy.P.phi.pml:184 Recv ACK	<- queue 2 (BtoN)
 93:	proc  2 (daisy:1) daisy.P.phi.pml:188 Sent FIN	-> queue 3 (NtoA)
 94:	proc  0 (peerA:1) daisy.P.phi.pml:38 Recv FIN	<- queue 3 (NtoA)
 96:	proc  1 (peerB:1) daisy.P.phi.pml:118 Send ACK	-> queue 2 (BtoN)
 98:	proc  2 (daisy:1) daisy.P.phi.pml:184 Recv ACK	<- queue 2 (BtoN)
102:	proc  0 (peerA:1) daisy.P.phi.pml:38 Send ACK	-> queue 4 (AtoN)
104:	proc  2 (daisy:1) daisy.P.phi.pml:181 Recv ACK	<- queue 4 (AtoN)
106:	proc  2 (daisy:1) daisy.P.phi.pml:191 Sent FIN	-> queue 1 (NtoB)
107:	proc  1 (peerB:1) daisy.P.phi.pml:118 Recv FIN	<- queue 1 (NtoB)
109:	proc  1 (peerB:1) daisy.P.phi.pml:118 Send ACK	-> queue 2 (BtoN)
111:	proc  2 (daisy:1) daisy.P.phi.pml:184 Recv ACK	<- queue 2 (BtoN)
117:	proc  0 (peerA:1) daisy.P.phi.pml:37 Send FIN	-> queue 4 (AtoN)
119:	proc  2 (daisy:1) daisy.P.phi.pml:182 Recv FIN	<- queue 4 (AtoN)
121:	proc  2 (daisy:1) daisy.P.phi.pml:191 Sent FIN	-> queue 1 (NtoB)
122:	proc  1 (peerB:1) daisy.P.phi.pml:118 Recv FIN	<- queue 1 (NtoB)
124:	proc  1 (peerB:1) daisy.P.phi.pml:118 Send ACK	-> queue 2 (BtoN)
126:	proc  2 (daisy:1) daisy.P.phi.pml:184 Recv ACK	<- queue 2 (BtoN)
130:	proc  2 (daisy:1) daisy.P.phi.pml:188 Sent FIN	-> queue 3 (NtoA)
131:	proc  0 (peerA:1) daisy.P.phi.pml:43 Recv FIN	<- queue 3 (NtoA)
Never claim moves to line 14	[((!((((state[0]==4)||(state[0]==5))||(state[0]==0)))&&(b==1)))]
Never claim moves to line 10	[(!((((state[0]==4)||(state[0]==5))||(state[0]==0))))]
139:	proc  0 (peerA:1) daisy.P.phi.pml:43 Send ACK	-> queue 4 (AtoN)
141:	proc  2 (daisy:1) daisy.P.phi.pml:200 Recv ACK	<- queue 4 (AtoN)
spin: trail ends after 143 steps
#processes: 3
		state[0] = 8
		state[1] = 8
		pids[0] = 0
		pids[1] = 0
		queue 4 (AtoN): 
		queue 2 (BtoN): 
		b = 1
143:	proc  2 (daisy:1) daisy.P.phi.pml:200 (state 21)
143:	proc  1 (peerB:1) daisy.P.phi.pml:117 (state 19)
143:	proc  0 (peerA:1) daisy.P.phi.pml:42 (state 19)
143:	proc  - (newPhi:1) _spin_nvr.tmp:9 (state 14)
3 processes created

*/