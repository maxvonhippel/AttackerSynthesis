[`↞` Back to **README.md**](../README.md), [`↞` Back to **Korg.md**](Korg.md)

# Interpreting Korg's Outputs

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
First of all, we can basically ignore the output in the command line.  This is just un-supressed Spin output.

What we are really interested is the output in `out/experiment1_False`.  Notice the naming scheme is `out/$(name)_$(with_recovery)`.