Tool (Korg), Models (TCP, etc.), and Documentation for Attacker Synthesis Project.

* TOC
{:toc}

## How to Read Docs

The documentation for this project consists of this README as well as all the files in `docs/`.  They natively link to one another so that you can navigate without ever using the file system.  These documents are written in [Github Markdown](https://developer.github.com/v3/markdown/) and are best viewed online on Github pages, [here](https://mxvh.pl/AttackerSynthesis).  We use features of Github flavor Markdown such as emojis, automatic tables of contents, and `HTML`.

* :clipboard: [`README.md` = this file](README.md)
	
	* :pushpin: [`Korg.md` = Korg tool overview](docs/Korg.md)
	* :pushpin: [`Install.md` = Korg install instuctions](docs/Install.md)
	* :pushpin: [`InterpretingOutputs.md` = details on Korg outputs](docs/InterpretingOutputs.md)
	* :pushpin: [`Troubleshooting.md` = troubleshooting tips for Korg](docs/Troubleshooting.md)
	* :pushpin: [`Usage.md` = usage instructions for Korg](docs/Usage.md)

## Repository Structure

This repository contains the tool `Korg` as well as various Promela models from our paper.  The most important parts from the paper are marked with a :pushpin:.

* `demo/` - contains models used for unit-testing the software, as well as our TCP model.
	- `emptyFile` is an empty file used in unit-testing.
	- `livenessExample1/` is a small example used in unit-testing.  It includes the liveness property `Phi.pml`.
	- `livenessExample2/` is a small example used in unit-testing.  It includes the properties:
		-- `phi.pml` a liveness property;
		-- `theta.pml` the trivial property; and
		-- `wrongPhi.pml` a safety property also used in unit-testing.
		-- the three properties `phi1.pml`, `phi2.pml`, `phi3.pml` used in the Case Study for `TM_1`, `TM_2`, `TM_3`.
	- `smallDemo1-3` are more small examples with explanations 
	- :pushpin: `TCP/` contains the entire TCP model used in our Case Study.
* `out/` - this is where the outputs of the program are written to.
* `results/` - this contains the results of the Case Study from the paper.  You can reproduce these results using the tool.
* `tests/` - this contains unit-test code for `Korg`.
* `__init__.py` - a file needed by Python to handle imports.
* :pushpin: `avgExperiment.sh` - a Bash script with which to reproduce our results in `results/`.

:pushpin: The rest of the contents of the repository are exactly the code for the tool `Korg`.

* `Characterize.py` - used to characterize models with respect to properties using `Spin`.
* `CLI.py` - handles basic I/O and CLI aspects of code.
* `Construct.py` - builds `Promela` models.
* `Korg.py` - the main code file for the tool.  Drives the rest of the code.
* `Makefile` - a Makefile containing various useful commands for using the tool, and for cleaning up afterword.
* `README` - this README.

## How to run an example
From the top-level to run smallDemo1, run the command `python3 Korg.py --name=smallDemo1 --dir='demo/smallDemo1/*'`. The output of the demo will appear in `out/smallDemo1`. You can change what directory the results appear in by changing the `name` flag.

## How to cite

Coming soon.

## ArXiV version with proofs.

Coming soon.

## How to use the tool.

See [`docs/Korg.md`](docs/Korg.md).
