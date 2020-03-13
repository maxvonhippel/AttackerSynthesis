.PHONY: demo

clean:
	- rm -rf out/*
	- rm *.trail
	- rm *.pml
	- rm ./*.pml
	- rm *pan*
	- rm *.tcl
	- rm .*.swp
	- rm *.pyc
	- rm test_exp*
	- rm ._n_i_p_s_
	echo "All clean!"

# Tests on TCP w/ experiment1 (phi_1)
experiment1:
	time python3 Gen3.py                      \
			--model=demo/TCP/TCP.pml          \
			--phi=experiments/experiment1.pml \
			--Q=demo/TCP/network.pml          \
			--IO=demo/TCP/IO.txt              \
			--max_attacks=1                   \
			--finite=False                    \
			--name=experiment1                \
			--characterize=False

# Reproduces our results fromthe Case Study
avgExperiment:
	for exp in 3 2 1; do                                                             \
		for b in False True; do                                                      \
			for n in 1 2 3 4 5 6 7 8 9 10; do                                        \
				rm *.pml;                                                            \
				name="experiment"$$exp"_"$$n"_"$$b;                                  \
				echo "\n\n~~~~~~~~~~~~~ EXPERIMENT :: "$$name" ~~~~~~~~~~~~~~~\n\n"; \
				/usr/bin/time -o "logs/"$$name"_log.txt" python3 Gen3.py             \
					--model=demo/TCP/TCP.pml                                         \
					--phi="experiments/experiment"$$exp".pml"                        \
					--Q=demo/TCP/network.pml                                         \
					--IO=demo/TCP/IO.txt                                             \
					--max_attacks=10                                                 \
					--finite=$$b                                                     \
					--name=$$name;                                                   \
			done;                                                                    \
		done;                                                                        \
	done;

# Runs the primary test class for Korg.py
testKorg: ; green tests/test_Korg.py

# Runs tests for Characterize.py
testChar: ; green tests/test_Characterize.py

# Runs tests for Construct.py
testCons: ; green tests/test_Construct.py

# Runs all tests
test: ; make clean testChar clean testKorg clean testCons

# Installs green so you can run the tests with my make targets
setup: ; pip3 install green