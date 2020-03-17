[`↞` Back to **README.md**](../README.md), [`↞` Back to **Korg.md**](Korg.md)

<p align="center">
<img
    title="Pictured: Korg Volca Beats, Bass, & Keys.  Image courtesy of Attack Magazine: https://www.attackmagazine.com/reviews/gear-software/korg-volca-beats-bass-keys/2/."
    style="border-radius: 50%; border: 2px solid black;" 
    src="images/multiple_korgs.png" 
    width="200">
</p>

# Interpreting Korg's Outputs

* TOC
{:toc}

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

1. Sends `ACK` over `NtoA`
2. Sends `SYN` over `NtoB`
3. Receives `SYN_ACK` over `BtoN`
4. Sends `ACK` over `NtoB`
5. Does nothing forever.

So, as a process, the attacker looks something like this.

````
              NtoA ! ACK             NtoB ! SYN
---> ( s_0 ) ------------> ( s_ 1) -------------> ( s_3 )
                                                    |
                                                    | BtoN ? SYN_ACK
                                     NtoB ! ACK     V
                           ( s_5 ) <------------- ( s_4 )
````

Note that this attacker has a trivial acceptance cycle.  But we can also make an attacker with a non-trivial acceptance cycle, like so.

> python3 Korg.py --model=demo/TCP/TCP.pml --phi=experiments/experiment2.pml --Q=demo/TCP/network.pml --IO=demo/TCP/IO.txt --max_attacks=3 --with_recovery=False --name=experiment2 --characterize=False

Inspecting `experiment2_False/attacker_2.pml`, I see:

````
/* spin -t2 -s -r experiment2_daisy_check.pml */
active proctype attacker() {
	
	NtoA ! ACK;
	NtoB ! ACK;
	// Acceptance Cycle part of attack
	do
	::
	   BtoN ? SYN;
	od
}
````

Clearly this attacker has a non-trivial acceptance cycle (again, using the paper's notation for the channels for my figure below):

````
               NtoA ! ACK           NtoB ! ACK
----> ( s_0 ) ------------> ( s_1 ) -----------> ( s_3 ) -----
                                                    ^        |
                                                    |        | BtoN ? SYN
                                                    ----------

                                               \_______ _________________/
                                                       V
                                            This is the non-trivial acceptance
                                            cycle.
````

## With `--characterize=True`

Running the code with `--characterize=True` does everything that Korg would do with `--characterize=False`, plus it saves the *artifacts* and writes a log file.  This is best explained via an example.  Suppose I run the following.

> python3 Korg.py --model=demo/TCP/TCP.pml --phi=experiments/experiment2.pml --Q=demo/TCP/network.pml --IO=demo/TCP/IO.txt --max_attacks=3 --with_recovery=True --name=experiment2 --characterize=True

So, I am running the same experiment as I did immediately previously, except with recovery, and with `--characterize=True`.  Then in `out/experiment2_True/`, I find the following.

````
(env) mvh:AttackerSynthesis$ tree out/experiment2_True/
out/experiment2_True/
├── artifacts
│   ├── attacker_0_WITH_RECOVERY_A.pml
│   ├── attacker_0_WITH_RECOVERY_E.pml
│   ├── attacker_1_WITH_RECOVERY_A.pml
│   ├── attacker_1_WITH_RECOVERY_E.pml
│   ├── attacker_2_WITH_RECOVERY_A.pml
│   └── attacker_2_WITH_RECOVERY_E.pml
├── attacker_0_WITH_RECOVERY.pml
├── attacker_1_WITH_RECOVERY.pml
├── attacker_2_WITH_RECOVERY.pml
└── log.txt

````

:scream: Wow!  :open_file_folder: That's a lot of files!  Let's go over what each of them is, exactly.

* :calendar: `attacker_0_WITH_RECOVERY.pml` is the first synthesized attacker, out of 3.  Obviously `attacker_1_WITH_RECOVERY.pml` is the second, and `attacker_2_WITH_RECOVERY.pml` is the third.

	* Actually, these three models are all exactly the same.  Sometimes I find that I need to run with a fairly large `--max_attacks` in order to get more than one *distinct* attacker.  The problem arises from non-determinism in `P`, or, in this case, `TCP.pml`.

* :spiral_notepad: `log.txt`.  This is a comma-separated-value (CSV) text file following the format `model,A/E,with_recovery?`.  So, column 1 gives the name of the attacker model (e.g., `attacker_0_WITH_RECOVERY.pml`); column 2 says `A-attack` if it is a ∀-attacker, `E-attack` if it is an ∃-attacker, or `NOT AN ATTACK` if somehow the code made a mistake (which should not happen ... so if this does happen, please file an issue in the [Issue Tracker](https://github.com/maxvonhippel/AttackerSynthesis/issues)); and column 3 says `True` iff it is an attacker with recovery, or `False` otherwise.

* :chart_with_upwards_trend: `artifacts/attacker_0_WITH_RECOVERY_A.pml` reports no violations or acceptance cycles when run with `spin -run -a`, if and only if `attacker_0_WITH_RECOVERY.pml` is a ∀-attacker.  Otherwise, it reports one or more violations or acceptance cycles.

	* Inspecting this file is a good way for you to understand *how* we check this.  The basic idea is to see if `P` composed with `attacker` *satisfies* the *negation* of `phi`.

	* Likewise, `artifacts/attacker_1_WITH_RECOVERY_A.pml` serves the same purpose for `attacker_1_WITH_RECOVERY.pml`, and, `artifacts/attacker_2_WITH_RECOVERY_A.pml` serves the same puspose for `attacker_2_WITH_RECOVERY.pml`.

* :clipboard: `artifacts/attacker_0_WITH_RECOVERY_E.pml` reports at least one violation or acceptance cycle iff `attacker_0_WITH_RECOVERY.pml` is an attacker.  So: 

	* if `spin -run -a artifacts/attacker_0_WITH_RECOVERY_E.pml` reports at least one violation or acceptance cycle, and `spin -run -a artifacts/attacker_0_WITH_RECOVERY_A.pml` does not, then `attacker_0_WITH_RECOVERY.pml` is a ∀-attacker;
	* if both commands report each at least one violation or acceptance cycle, then `attacker_0_WITH_RECOVERY.pml` is an ∃-attacker;
	* if neither command reports at least one violation or acceptance cycle, then there is something *very very wrong* with the code, and you should submit the inputs and outputs for us to inspect on the [Issue Tracker](https://github.com/maxvonhippel/AttackerSynthesis/issues);
	* likewise, if `spin -run -a artifacts/attacker_0_WITH_RECOVERY_E.pml` reports no violation or acceptance cycle, but `spin -run -a artifacts/attacker_0_WITH_RECOVERY_A.pml` reports at least one violation or acceptance cycle, then there is something *very very wrong* with the code, and you should submit the inputs and outputs for us to inspect on the [Issue Tracker](https://github.com/maxvonhippel/AttackerSynthesis/issues).
	* Obviously `artifacts/attacker_$n_WITH_RECOVERY_E.pml` and `artifacts_attacker_$n_WITH_RECOVERY_A.pml` serve the same respective purposes for the attacker `attacker_$n_WITH_RECOVERY.pml`, for `$n ∈ { 0, 1, 2 }`.

### `Ψ`

There is one more thing for us to notice here: `Ψ`.  In the paper, we take a property `Φ`, and we construct a new property `Ψ = (F recover) ⇒ Φ`.  We use a bit `b` to detect recovery in our models, like so:

````
bit b= 0;
active proctype daisy () {
	do
	:: AtoN?ACK;
	:: AtoN?FIN;
	:: AtoN?SYN;
	
	// etc etc etc

	:: break; // recovery to N ... 
	od
	b = 1;
	// N begins here ... 

	do
	:: AtoN ? SYN -> 
		if
		:: NtoB ! SYN;
		fi unless timeout;
	:: BtoN ? SYN -> 
		if
		:: NtoA ! SYN;
		fi unless timeout;
	
	// etc etc etc

	:: _nr_pr < 3 -> break;
	od
end:

}
````

Then, given a `Φ`, for example:

````
ltl exp2 {
	( (always ( eventually ( state[0] == 1 && state[1] == 2 ) ) ) 
		implies ( eventually ( state[0] == 4 ) ) )
}

````
... we can construct a `Ψ`, as evident at the top-level directory in `experiment2_daisy_check.pml`:

````
ltl newPhi {
	(eventually ( b == 1 ) ) implies
		
	( (always ( eventually ( state[0] == 1 && state[1] == 2 ) ) ) 
		implies ( eventually ( state[0] == 4 ) ) )
  ) )
}
````
However, we do not use this property in our `artifacts`, because we know that there must exist a violating run with `b == 1` in order for us to get a result in the first place.

If this worries you, you can add the bit `b` back in to the attacker before recovery, and run the artifacts with `Ψ`, and you should get the expected results.