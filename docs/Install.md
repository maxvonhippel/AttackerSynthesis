[`↞` Back to **README.md**](../README.md), [`↞` Back to **Korg.md**](Korg.md)

# Korg Installation Instructions

## Instructions

We have tried to make this easy by providing the installation script [`setup.sh`](../setup.sh).  

* Note: this script assumes `Python3` is already globally installed.

However, if this does not work for you, then:

1. Install <a href="www.spinroot.com">Spin</a> *globally*.  So, you should be able to run it from the command line from anywhere in your computer.
	
	* An easy way to confirm this is to run `spin` from some arbitrary folder in the command line, and see if something sensible happens! 

2. Make sure you have `Python3` installed.

	* An easy way to confirm this is to run `echo "print('awesome')" | python3` from some arbitrary folder in the command line, and see if the resulting output is, indeed, `awesome`.

3. `pip3 install green` so the tests will run correctly from the `Makefile`.

4. If somehow `make` is not installed on your system, consider installing it so you can use the `Makefile`!

5. Then to confirm everything is up and running, try `make test`, and see if you get a ton of output ending with confirmation that the tests passed!

	* See the example output at the bottom of this page.

If you have any questions, feel free to email me at maxvonhippel@gmail.com, or, open up an issue in the [Issue Tracker](https://github.com/maxvonhippel/AttackerSynthesis/issues).

## Example Test Output

Example output for `make test` is:

````
(env) mvh:AttackerSynthesis$ make test
rm -rf tests/__pycache__
rm -rf __pycache__
make clean testChar clean testKorg clean testCons
make[1]: Entering directory '/home/mvh/projects/research/AttackerSynthesis'
rm -rf out/*
rm *.trail
rm: cannot remove '*.trail': No such file or directory
Makefile:12: recipe for target 'clean' failed
make[1]: [clean] Error 1 (ignored)
rm *.pml
rm: cannot remove '*.pml': No such file or directory
Makefile:12: recipe for target 'clean' failed
make[1]: [clean] Error 1 (ignored)
rm ./*.pml
rm: cannot remove './*.pml': No such file or directory
Makefile:12: recipe for target 'clean' failed
make[1]: [clean] Error 1 (ignored)
rm *pan*
rm: cannot remove '*pan*': No such file or directory
Makefile:12: recipe for target 'clean' failed
make[1]: [clean] Error 1 (ignored)
rm *.tcl
rm: cannot remove '*.tcl': No such file or directory
Makefile:12: recipe for target 'clean' failed
make[1]: [clean] Error 1 (ignored)
rm .*.swp
rm: cannot remove '.*.swp': No such file or directory
Makefile:12: recipe for target 'clean' failed
make[1]: [clean] Error 1 (ignored)
rm *.pyc
rm: cannot remove '*.pyc': No such file or directory
Makefile:12: recipe for target 'clean' failed
make[1]: [clean] Error 1 (ignored)
rm test_exp*
rm: cannot remove 'test_exp*': No such file or directory
Makefile:12: recipe for target 'clean' failed
make[1]: [clean] Error 1 (ignored)
rm ._n_i_p_s_
rm: cannot remove '._n_i_p_s_': No such file or directory
Makefile:12: recipe for target 'clean' failed
make[1]: [clean] Error 1 (ignored)
echo "All clean!"
All clean!
green tests/test_Characterize.py
.....

Captured stdout for tests.test_Characterize.TestCharacterize.test_violate_exp1
Search depth was too small at 10000  doubling depth ...
Search depth was too small at 20000  doubling depth ...

Ran 5 tests in 37.003s using 8 processes

OK (passes=5)
make[1]: 'clean' is up to date.
green tests/test_Korg.py
.....ltl eventuallyAlwaysWEqualZero: <> ([] ((w==0)))
pan:1: acceptance cycle (at depth 0)
pan: wrote test_works_on_Liveness_False_daisy_check.pml.trail

(Spin Version 6.5.0 -- 17 July 2019)
Warning: Search not completed
	+ Partial Order Reduction

Full statespace search for:
	never claim         	+ (eventuallyAlwaysWEqualZero)
	assertion violations	+ (if within scope of claim)
	acceptance   cycles 	+ (fairness disabled)
	invalid end states	- (disabled by never claim)

State-vector 36 byte, depth reached 12, errors: 1
        5 states, stored (8 visited)
        3 states, matched
       11 transitions (= visited+matched)
        0 atomic steps
hash conflicts:         0 (resolved)

Stats on memory usage (in Megabytes):
    0.000	equivalent memory usage for states (stored*(State-vector + overhead))
    0.290	actual memory usage for states
  128.000	memory used for hash table (-w24)
    0.534	memory used for DFS stack (-m10000)
  128.730	total actual memory usage



pan: elapsed time 0 seconds
.ltl eventuallyAlwaysWEqualZero: <> ([] ((w==0)))
pan:1: acceptance cycle (at depth 0)
pan: wrote test_works_on_Coles_example_False_daisy_check.pml.trail

(Spin Version 6.5.0 -- 17 July 2019)
Warning: Search not completed
	+ Partial Order Reduction

Full statespace search for:
	never claim         	+ (eventuallyAlwaysWEqualZero)
	assertion violations	+ (if within scope of claim)
	acceptance   cycles 	+ (fairness disabled)
	invalid end states	- (disabled by never claim)

State-vector 36 byte, depth reached 12, errors: 1
        5 states, stored (8 visited)
        3 states, matched
       11 transitions (= visited+matched)
        0 atomic steps
hash conflicts:         0 (resolved)

Stats on memory usage (in Megabytes):
    0.000	equivalent memory usage for states (stored*(State-vector + overhead))
    0.290	actual memory usage for states
  128.000	memory used for hash table (-w24)
    0.534	memory used for DFS stack (-m10000)
  128.730	total actual memory usage



pan: elapsed time 0 seconds
.ltl newPhi: [] ((! ((b==1))) || ([] ((! ((state[0]==0))) || (! ((state[1]==4))))))
pan:1: assertion violated  !(( !( !((b==1)))&& !(( !((state[0]==0))|| !((state[1]==4)))))) (at depth 86)
pan: wrote test_works_on_TCP_exp1_True_daisy_check.pml.trail

(Spin Version 6.5.0 -- 17 July 2019)
Warning: Search not completed
	+ Partial Order Reduction

Full statespace search for:
	never claim         	+ (newPhi)
	assertion violations	+ (if within scope of claim)
	acceptance   cycles 	+ (fairness disabled)
	invalid end states	- (disabled by never claim)

State-vector 108 byte, depth reached 325, errors: 1
    33462 states, stored
    57861 states, matched
    91323 transitions (= stored+matched)
        0 atomic steps
hash conflicts:        38 (resolved)

Stats on memory usage (in Megabytes):
    4.340	equivalent memory usage for states (stored*(State-vector + overhead))
    3.002	actual memory usage for states (compression: 69.16%)
         	state-vector as stored = 66 byte + 28 byte overhead
  128.000	memory used for hash table (-w24)
    0.611	memory used for DFS stack (-m10000)
  131.540	total actual memory usage



pan: elapsed time 0.05 seconds
pan: rate    669240 states/second
ltl exp1: [] ((! ((state[0]==0))) || (! ((state[1]==4))))
pan:1: assertion violated  !( !(( !((state[0]==0))|| !((state[1]==4))))) (at depth 36)
pan: wrote test_works_on_TCP_exp1_False_daisy_check.pml.trail

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



pan: elapsed time 0 seconds
.ltl newPhi: [] ((! ((b==1))) || ((! ([] (<> (((state[0]==1)) && ((state[1]==2)))))) || (<> ((state[0]==4)))))
pan:1: acceptance cycle (at depth 58)
pan: wrote test_works_on_TCP_exp2_True_daisy_check.pml.trail

(Spin Version 6.5.0 -- 17 July 2019)
Warning: Search not completed
	+ Partial Order Reduction

Full statespace search for:
	never claim         	+ (newPhi)
	assertion violations	+ (if within scope of claim)
	acceptance   cycles 	+ (fairness disabled)
	invalid end states	- (disabled by never claim)

State-vector 108 byte, depth reached 151, errors: 1
      279 states, stored (280 visited)
       90 states, matched
      370 transitions (= visited+matched)
        0 atomic steps
hash conflicts:         0 (resolved)

Stats on memory usage (in Megabytes):
    0.036	equivalent memory usage for states (stored*(State-vector + overhead))
    0.267	actual memory usage for states
  128.000	memory used for hash table (-w24)
    0.611	memory used for DFS stack (-m10000)
  128.806	total actual memory usage



pan: elapsed time 0 seconds
ltl exp2: (! ([] (<> (((state[0]==1)) && ((state[1]==2)))))) || (<> ((state[0]==4)))
pan:1: acceptance cycle (at depth 28)
pan: wrote test_works_on_TCP_exp2_False_daisy_check.pml.trail

(Spin Version 6.5.0 -- 17 July 2019)
Warning: Search not completed
	+ Partial Order Reduction

Full statespace search for:
	never claim         	+ (exp2)
	assertion violations	+ (if within scope of claim)
	acceptance   cycles 	+ (fairness disabled)
	invalid end states	- (disabled by never claim)

State-vector 108 byte, depth reached 61, errors: 1
       37 states, stored (39 visited)
        7 states, matched
       46 transitions (= visited+matched)
        0 atomic steps
hash conflicts:         0 (resolved)

Stats on memory usage (in Megabytes):
    0.005	equivalent memory usage for states (stored*(State-vector + overhead))
    0.282	actual memory usage for states
  128.000	memory used for hash table (-w24)
    0.534	memory used for DFS stack (-m10000)
  128.730	total actual memory usage



pan: elapsed time 0 seconds
.

Captured stdout for tests.test_Korg.TestKorg.test_errors_if_IO_None
We could not find any inputs or outputs in dne.blarg; giving up.
We could not find any inputs or outputs in demo/emptyFile; giving up.
We could not find any inputs or outputs in dne.blarg; giving up.
We could not find any inputs or outputs in demo/emptyFile; giving up.

Captured stdout for tests.test_Korg.TestKorg.test_errors_if_cannot_negate_phi
No property phi provided; giving up.
No property phi provided; giving up.

Captured stdout for tests.test_Korg.TestKorg.test_errors_if_no_attackers_requested
--num option must be > 0, was: 0; giving up.
--num option must be > 0, was: 0; giving up.

Captured stdout for tests.test_Korg.TestKorg.test_errors_if_no_solution
We could not find any with_recovery(model, (N), phi)-attacker A.
We could not find any (model, (N), phi)-attacker A.

Captured stdout for tests.test_Korg.TestKorg.test_errors_if_trivial
In order for the problem (model, phi, N) to be non-trivial, we 		   require that (model || N) |= phi.  However, this does not appear 		   to be the case.
In order for the problem (model, phi, N) to be non-trivial, we 		   require that (model || N) |= phi.  However, this does not appear 		   to be the case.

Captured stdout for tests.test_Korg.TestKorg.test_on_Liveness
We could not find any with_recovery(model, (N), phi)-attacker A.

Captured stdout for tests.test_Korg.TestKorg.test_works_on_Coles_example
We could not find any with_recovery(model, (N), phi)-attacker A.

Ran 9 tests in 72.915s using 8 processes

OK (passes=9)
make[1]: 'clean' is up to date.
green tests/test_Construct.py
...

Ran 3 tests in 0.112s using 8 processes

OK (passes=3)
make[1]: Leaving directory '/home/mvh/projects/research/AttackerSynthesis'

````