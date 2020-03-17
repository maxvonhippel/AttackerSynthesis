[`↞` Back to **README.md**](../README.md), [`↞` Back to **Korg.md**](Korg.md)

# Interpreting Korg's Outputs

<p align="center">
	Pictured: Korg Volca Beats, Bass, & Keys.  Image courtesy of <a href="https://www.attackmagazine.com/reviews/gear-software/korg-volca-beats-bass-keys/2/">Attack Magazine</a>.
	<br><br>
	<img src="images/multiple_korgs.png">
</p>

## With `--characterize=False`

Suppose I run Korg wit the following parameters.

* `--model=demo/TCP/TCP.pml`
* `--phi=experiments/experiment1.pml`
* `--Q=demo/TCP/network.pml`
* `--IO=demo/TCP/IO.txt`
* `--max_attacks=1`
* `--with_recovery=False`
* `--name=experiment1`
* `--characterize=False`

Like this:

````
(env) mvh:AttackerSynthesis$ python3 Korg.py --model=demo/TCP/TCP.pml --phi=experiments/experiment1.pml --Q=demo/TCP/network.pml --IO=demo/TCP/IO.txt --max_attacks=1 --with_recovery=False --name=experiment1 --characterize=False
ltl exp1: [] ((! ((state[0]==0))) || (! ((state[1]==4))))
pan:1: assertion violated  !( !(( !((state[0]==0))|| !((state[1]==4))))) (at depth 36)
pan: wrote experiment1_daisy_check.pml.trail

(Spin Version 6.5.0 -- 17 July 2019)
Warning: Search not completed
	+ Partial Order Reduction

Full statespace search for:
	never claim         	+ (exp1)
	assertion violations	+ (if within scope of claim)
	acceptance   cycles 	+ (fairness disabled)
	invalid end states	- (disabled by never claim)

State-vector 108 byte, depth reached 359, errors: 1
     3742 states, stored
     7291 states, matched
    11033 transitions (= stored+matched)
        0 atomic steps
hash conflicts:         2 (resolved)

Stats on memory usage (in Megabytes):
    0.485	equivalent memory usage for states (stored*(State-vector + overhead))
    0.575	actual memory usage for states
  128.000	memory used for hash table (-w24)
    0.534	memory used for DFS stack (-m10000)
  129.022	total actual memory usage



pan: elapsed time 0.01 seconds
````
First of all, we can basically ignore the output in the command line.  This is just unsuppressed Spin output.

What we are really interested is the output in `out/experiment1_False`.  Notice the naming scheme is `out/$(name)_$(with_recovery)`.

````
(env) mvh:AttackerSynthesis$ tree out
out
└── experiment1_False
    └── attacker_0.pml

1 directory, 1 file

````
Let's look at `attacker_0.pml`.

````
/* spin -t -s -r experiment1_daisy_check.pml */
active proctype attacker() {
	
	NtoA ! ACK;
	NtoB ! SYN;
	BtoN ? SYN_ACK;
	NtoB ! ACK;
	// Acceptance Cycle part of attack
}
````
The first line gives the command that was used to produce the trail file which was interpreted in order to synthesize this attacker.  The rest of the lines give us the `attacker()` process, which, in order:

1. Sends `ACK` over `NtoA` (called `Nto1` in the paper);
2. Sends `SYN` over `NtoB` (called `Nto2` in the paper);
3. Receives `SYN_ACK` over `BtoN` (called `2toN` in the paper);
4. Sends `ACK` over `NtoB` (called `Nto2` in the paper);
5. Does nothing forever.

So, as a process, the attacker looks something like this.

````
              Nto1 ! ACK             Nto2 ! SYN
---> ( s_0 ) ------------> ( s_ 1) -------------> ( s_3 )
                                                    |
                                                    | 2toN ? SYN_ACK
                                     Nto2 ! ACK     V
                           ( s_5 ) <------------- ( s_4 )
````

Note that this attacker has a trivial acceptance cycle.  But we can also make an attacker with a non-trivial acceptance cycle, like so.

TODO