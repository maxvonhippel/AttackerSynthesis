# ==============================================================================
# File      : Makefile
# Author    : Max von Hippel
# Authored  : 13 March 2020
# Purpose   : provides various useful targets for running Korg
# How to run: see https://www.gnu.org/software/make/manual/make.html if you are
#             unfamiliar with Makefiles.
# ==============================================================================

# Deletes all the left-over files produced by running the other targets in this file.
clean:
	- rm -rf __pycache__
	- rm -rf tests/__pycache__
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
	- rm **.tmp
	- rm *.txt
	echo "All clean!"

# -------------------------------------------------------------------------------
# DCCP and TCP targets are canonical versions from Case Studies in RFC NLP paper.
# Choice of max_attacks=100 is because that's what we did in RFC NLP.
# -------------------------------------------------------------------------------

dccp:
	for j in 1 2 3 4; do               \
		python3 korg/Korg.py           \
			--model=demo/DCCP/DCCP.pml \
			--phi=demo/DCCP/phi$$j.pml \
			--Q=demo/DCCP/network.pml  \
			--IO=demo/DCCP/IO.txt      \
			--max_attacks=100          \
			--with_recovery=True       \
			--name=DCCP.$$j            \
			--characterize=False;      \
	done;

tcp:
	for j in 1 2 3 4; do               \
		python3 korg/Korg.py           \
			--model=demo/TCP/TCP.pml   \
			--phi=demo/TCP/phi$$j.pml  \
			--Q=demo/TCP/network.pml   \
			--IO=demo/TCP/IO.txt       \
			--max_attacks=100          \
			--with_recovery=True       \
			--name=TCP.$$j             \
			--characterize=False;      \
	done;

# -------------------------------------------------------------------------------
# The remaining targets are from the original KORG paper.
# -------------------------------------------------------------------------------

# Tests on TCP w/ experiment1 (phi_1)
experiment1:
	time python3 korg/Korg.py                 \
			--model=demo/TCP/TCP.pml          \
			--phi=demo/TCP/phi1.pml 		  \
			--Q=demo/TCP/network.pml          \
			--IO=demo/TCP/IO.txt              \
			--max_attacks=1                   \
			--with_recovery=False             \
			--name=experiment1                \
			--characterize=False

# Runs the semaphore demo
semaphoreDemo:
	python3 korg/Korg.py \
		--model=demo/smallDemo4/Alice.pml \
		--phi=demo/smallDemo4/Phi.pml     \
		--Q=demo/smallDemo4/Bob.pml       \
		--IO=demo/smallDemo4/IO.txt       \
		--max_attacks=1                   \
		--with_recovery=False             \
		--name=semaphoreDemo              \
		--characterize=True

# Reproduces our results from the Case Study
avgExperiment:
	mkdir -p logs;                                                                   \
	for exp in 3 2 1; do                                                             \
		for b in False True; do                                                      \
			for n in 1 2 3 4 5 6 7 8 9 10; do                                        \
				rm *.pml;                                                            \
				name="experiment"$$exp"_"$$n"_"$$b;                                  \
				echo "\n\n~~~~~~~~~~~~~ EXPERIMENT :: "$$name" ~~~~~~~~~~~~~~~\n\n"; \
				touch "logs/"$$name"_log.txt";                                       \
				/usr/bin/time -o "logs/"$$name"_log.txt" python3 korg/Korg.py        \
					--model=demo/TCP/TCP.pml                                         \
					--phi="demo/TCP/phi"$$exp".pml"                                  \
					--Q=demo/TCP/network.pml                                         \
					--IO=demo/TCP/IO.txt                                             \
					--max_attacks=10                                                 \
					--with_recovery=$$b                                              \
					--name=$$name;                                                   \
			done;                                                                    \
		done;                                                                        \
	done;

# Runs the primary test class for korg/Korg.py
testKorg: ; green korg/tests/test_korg/Korg.py

# Runs tests for Characterize.py
testChar: ; green korg/tests/test_Characterize.py

# Runs tests for Construct.py
testCons: ; green korg/tests/test_Construct.py

# Runs all tests
test: 
	rm -rf tests/__pycache__
	rm -rf __pycache__
	make clean testChar clean testKorg clean testCons

# create new example directory
# `make newExample dir=new_dir_name`
newExample: 
	- mkdir ${dir} 
	- cd ${dir}
	- touch P.pml Q.pml IO.txt Phi.pml