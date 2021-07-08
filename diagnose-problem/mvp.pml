int b = 0;

chan blarg = [0] of { int };

active proctype banana() {

	blarg ! 1;

	blarg ? 2;

	blarg ! 3;

	do
	:: blarg ? 4;
	od

}

active proctype demo() {

	blarg ? 1;

	b = 1;

	blarg ! 2;

	b = 2;

	blarg ? 3;

	do
	:: b = 5; blarg ! 4;
	od
}

ltl bn5 {
	always (b != 5)
}

/*

(base) max@max-XPS-13-9310:~/projects/research/nds2/korg/diagnose-problem$ spin -t0 -s -r -p -g mvp.pml
ltl bn5: [] ((b!=5))
starting claim 2
Never claim moves to line 4	[(1)]
  2:	proc  0 (banana:1) mvp.pml:7 Sent 1	-> queue 1 (blarg)
  2:	proc  0 (banana:1) mvp.pml:7 (state 1)	[blarg!1]
  3:	proc  1 (demo:1) mvp.pml:21 Recv 1	<- queue 1 (blarg)
  3:	proc  1 (demo:1) mvp.pml:21 (state 1)	[blarg?1]
  5:	proc  1 (demo:1) mvp.pml:23 (state 2)	[b = 1]
		b = 1
  7:	proc  1 (demo:1) mvp.pml:25 Sent 2	-> queue 1 (blarg)
  7:	proc  1 (demo:1) mvp.pml:25 (state 3)	[blarg!2]
  8:	proc  0 (banana:1) mvp.pml:9 Recv 2	<- queue 1 (blarg)
  8:	proc  0 (banana:1) mvp.pml:9 (state 2)	[blarg?2]
 10:	proc  1 (demo:1) mvp.pml:27 (state 4)	[b = 2]
		b = 2
 12:	proc  0 (banana:1) mvp.pml:11 Sent 3	-> queue 1 (blarg)
 12:	proc  0 (banana:1) mvp.pml:11 (state 3)	[blarg!3]
 13:	proc  1 (demo:1) mvp.pml:29 Recv 3	<- queue 1 (blarg)
 13:	proc  1 (demo:1) mvp.pml:29 (state 5)	[blarg?3]
 15:	proc  1 (demo:1) mvp.pml:32 (state 6)	[b = 5]
		b = 5
spin: _spin_nvr.tmp:3, Error: assertion violated
spin: text of failed assertion: assert(!(!((b!=5))))
Never claim moves to line 3	[assert(!(!((b!=5))))]
spin: trail ends after 16 steps
#processes: 2
		b = 5
 16:	proc  1 (demo:1) mvp.pml:32 (state 7)
 16:	proc  0 (banana:1) mvp.pml:13 (state 5)
 16:	proc  - (bn5:1) _spin_nvr.tmp:2 (state 6)
2 processes created


Notice that with the -p option, we get the line b = 1, representing the beginning of the recovery.

*/