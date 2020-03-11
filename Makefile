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

# Tests on TCP
experiment1:
	time python3 Gen3.py                      \
			--model=demo/TCP/TCP.pml          \
			--phi=experiments/experiment1.pml \
			--Q=demo/TCP/network.pml          \
			--IO=demo/TCP/IO.txt              \
			--max_attacks=1                  \
			--finite=False                    \
			--name=experiment1                \
			--characterize=False

# Tests on TCP
experiment3:
	time python3 Gen3.py                      \
			--model=demo/TCP/TCP.pml          \
			--phi=experiments/experiment3.pml \
			--Q=demo/TCP/network.pml          \
			--IO=demo/TCP/IO.txt              \
			--max_attacks=1                   \
			--finite=False                    \
			--name=experiment3                \
			--characterize=False

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

experiment2:
	python3 Gen3.py                       \
		--model=demo/TCP/TCP.pml          \
		--phi=experiments/experiment2.pml \
		--Q=demo/TCP/network.pml          \
		--IO=demo/TCP/IO.txt              \
		--max_attacks=5                   \
		--finite=False                    \
		--name=experiment2

testG3:
	green tests/test_Gen3.py

testChar:
	green tests/test_Characterize.py

testCons:
	green tests/test_Construct.py


test:
	make clean testChar clean testG3 clean testCons

setup: ; pip3 install green # TODO: replace with a real dependency system ...

demo:
	make demoSafety demoLiveness demoLiveness2
