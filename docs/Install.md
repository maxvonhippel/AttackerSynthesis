# Korg Installation Instructions

We have tried to make this easy by providing the installation script [`setup.sh`](../install.sh).  However, if this does not work for you, then:

1. Install [Spin](www.spinroot.com) *globally*.  So, you should be able to run it from the command line from anywhere in your computer.
	* If you are unsure if you have successfully done this, just open a terminal, and type `mkdir demo && cd demo && spin`, and see if you get some output like 

	> Spin Version 6.5.0 -- 17 July 2019
	  spin: error, no filename specified

2. Make sure you have `Python3` installed.

3. `pip3 install green` so the tests will run correctly from the `Makefile`.

4. If somehow `make` is not installed on your system, consider installing it so you can use the `Makefile`!

5. Then to confirm everything is up and running, try `make test`, and see if you get a ton of output ending with confirmation that the tests passed!

If you have any questions, feel free to email me at maxvonhippel@gmail.com, or, open up an issue in the Github Issue Tracker.