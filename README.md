# AttackerSynthesis

Tool, Models, and Supplementary Materials for Attacker Synthesis Project.

**This repository is currently in flux.  In the near future, the repository will be updated with full documentation, and cleaner code.  At that time this README will be updated accordingly.**

**REPOSITORY STATUS:**

* Documentation: *in progress* :expressionless:
* Citation: *coming soon* :zipper_mouth_face:
* ArXiV version: *coming soon* :zipper_mouth_face:
* Instructions for using `Korg`: *coming soon* :zipper_mouth_face:
* `Korg` passing tests: *in progress* :expressionless:
* Makefile working: *coming soon* :zipper_mouth_face:
* `Korg` CLI improved: *coming soon* :zipper_mouth_face:

## Repository Structure

This repository contains the tool `Korg` as well as various Promela models from our paper.

* `demo/` - contains models used for unit-testing the software, as well as our TCP model.
	- `emptyFile` is an empty file used in unit-testing.
	- `livenessExample1/` is a small example used in unit-testing.  It includes the liveness property `Phi.pml`.
	- `livenessExample2/` is a small example used in unit-testing.  It includes the properties:
		-- `phi.pml` a liveness property;
		-- `theta.pml` the trivial property; and
		-- `wrongPhi.pml` a safety property also used in unit-testing.
	- `TCP/` contains the entire TCP model used in our Case Study.
* `experiments/` - contains the three properties `phi_1.pml`, `phi_2.pml`, `phi_3.pml` used in the Case Study for `TM_1`, `TM_2`, `TM_3`.
* `out/` - this is where the outputs of the program are written to.
* `results/` - this contains the results of the Case Study from the paper.  You can reproduce these results using the tool.
* `tests/` - this contains unit-test code for `Korg`.
* `__init__.py` - a file needed by Python to handle imports.
* `avgExperiment.sh` - a Bash script with which to reproduce our results in `results/`.

The rest of the contents of the repository are exactly the code for the tool `Korg`.

* `Characterize.py` - used to characterize models with respect to properties using `Spin`.
* `CLI.py` - handles basic I/O and CLI aspects of code.
* `Construct.py` - builds `Promela` models.
* `Korg.py` - the main code file for the tool.  Drives the rest of the code.
* `Makefile` - a Makefile containing various useful commands for using the tool, and for cleaning up afterword.
* `README` - this README.

## How to cite

Coming soon.

## ArXiV version with proofs.

Coming soon.

## How to use the tool.

See [`docs/Korg.md`](docs/Korg.md).
