[`↞` Back to **README.md**](../README.md), [`↞` Back to **Korg.md**](Korg.md)

# How to use Korg

<p align="center">
  Pictured: Korg NuTekt synth.  Image courtesy of <a href="https://store.attackmagazine.com/products/korg-nts-1-digital-kit">Attack Magazine</a>.
  <br><br>
  <img src="images/Korg_NuTekt.png">
</p>

## As a Tool

As a tool, Korg should be used through the command line (Bash).

* Yes, it almost certainly works fine in variants such as [ZSH](https://ohmyz.sh/).  But if you have any difficulties along these lines, feel free to tell us about it in the [Issue Tracker](https://github.com/maxvonhippel/AttackerSynthesis/issues), and we will try to help.

The Korg usage is as follows.

````
python3 Korg.py --model=$1 
		--phi=$2 
		--Q=$3 --IO=$4 
		--max_attacks=$5 
		--with_recovery=$6 
		--name=$7 
		--characterize=$8
````

We break down these arguments below.  Required parameters are marked with a :japanese_ogre:, while optional parameters are marked with a :ghost:.  Arguments may be given in any order.

* :japanese_ogre: `$1` is the system model, e.g., [`TCP.pml`](../demo/TCP/TCP.pml).  

	* This is what we call `M` in the paper.

* :japanese_ogre: `$2` is the property the attacker wants to violate, e.g., [`experiment1.pml`](../experiments/experiment1.pml).  

	* This is what we call `Φ` in the paper, and should be written in linear temporal logic.

* :japanese_ogre: `$3` is the vulnerable process that the attacker will replace, e.g., [`network.pml`](../demo/TCP/network.pml).  

	* This is what we call `Q` in the paper in the centralized-attacker case, as in, `TM = (P, (Q), Φ)`.
	* In other words, the threat model is `TM = ($1, ($3), $2)`.

* :japanese_ogre: `$4` is the `IO` file.  

	* The grammar of this file is outlined in the IO section a little below in this document.  Its purpose is to specify what messages the attacker (or `Q`) can receive or send and over what channels.  For example, see [`IO.txt`](../demo/TCP/IO.txt).

* :japanese_ogre: `$5` is the *maximum* number of attackers Korg should synthesize.  

	* Korg can make many many attackers, and often it will generate many very similar or even identical attackers, for subtle reasons having to do with how the trail files are interpreted, so it is a good idea to set this number fairly low until you have a strong grasp of how to best use the tool.  I typically like to use `--max_attacks=10`.

* :ghost: `$6` is `True` if you want to solve the `R∃ASP` (that is, the ∃-problem with recovery), or `False` if you want to solve the `∃ASP` (that is, the ∃-problem without recovery).  

	* I tend to find attackers with recovery more interesting, but it is generally a good idea to try running it both ways as sometimes attackers with recovery might not exist but attackers without recovery do.

* :japanese_ogre: `$7` is the name you want to be used for the folder in `out/` where all the outputs will be written.  

	* It is usually a good idea to pick something particular to your specific experiment, so you can find your results later on after you have run Korg many times.  For some examples, see the names used in our [tests](../tests/test_Korg.py).  For more documentation on these outputs, see [`InterpretingOutputs.md`](InterpretingOutputs.md).

* :ghost: `$8` is `True` if you want to have artifacts generated with which to assess the quality and type of your synthesized attackers.  

	* For more on these artifacts, see [`InterpretingOutputs.md`](InterpretingOutputs.md).  Note that setting this to `True` will slow down Korg, possibly by quite a lot (as in `TM_3` in the paper, which corresponds to [`experiment3.pml`](../experiments/experiment3.pml)).  I usually tun the experiment with this `False` first, and then try again with it `True`.

#### IO File Grammar / Syntax

The syntax of the IO file is:

````
chan1:
	I:a1,a2,...
	O:b1',b2',...
chan2:
	I:c1,c2,...
	O:d1,d2,...
...
````

In other words, for each channel :ear: that the process can communicate over, you have a new line 

> :ear::

followed by a newline and a tab, then `I:` and a comma-seperated list of the inputs the process can hear over :ear:, followed by a newline and then a tab and then `O:` and a comma-seperated list of the outputs the process can send over :ear:.

We assume that when you provide Korg with an interface, it is the interface of the `Q` argument, however, we do not computationally enforce this assumption.  (Your results might not make sense if this assumption is not met.)

## As a Library

Korg can be used as a Python library.

````
from Korg import *
````

The best way to see how to do this is to look at the unit tests, e.g., [`test_Korg.py`](../tests/test_Korg.py), which do exactly this.

* If you use Korg in your project, please let us know!  We would love to see how you use it.