Tool (Korg), Models (TCP, etc.), and Documentation for Attacker Synthesis Project, *with modifications to support RFCNLP paper*.

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
* `example.attacks/` - contains example outputs for different threat models.
	- `dccp/` - example attacks for canonical DCCP model from RFCNLP paper.
	- `redo.korg.results/` - what you get if you re-run the KORG ArXiV Case Study using the latest version of KORG, which has partial order reduction turned off in order to support RFCNLP and other projects./
	- `redo.korg.results.with.partial.order.reduction/` - the results from the KORG ArXiV Case Study.
	- `tcp/` - the updated canonical TCP model we used in the RFCNLP paper.
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

To cite KORG or the TCP model, please use the following BibTeX:

````
@misc{hippel2020automated,
    title={Automated Attacker Synthesis for Distributed Protocols},
    author={Max von Hippel and Cole Vick and Stavros Tripakis and Cristina Nita-Rotaru},
    year={2020},
    eprint={2004.01220},
    archivePrefix={arXiv},
    primaryClass={cs.CR}
}
````

For more, view the article in [Semantic Scholar](https://api.semanticscholar.org/CorpusID:214795205).  To cite the DCCP model, please use the following BibTeX:

````
@article{pacheco2022automated,
  title={Automated Attack Synthesis by Extracting Finite State Machines from Protocol Specification Documents},
  author={Pacheco, Maria Leonor and von Hippel, Max and Weintraub, Ben and Goldwasser, Dan and Nita-Rotaru, Cristina},
  journal={arXiv preprint arXiv:2202.09470},
  year={2022}
}
````


## ArXiV version with proofs.

Available [here](https://arxiv.org/abs/2004.01220).  You can reproduce the results by building the [Dockerfile](Dockerfile), which will compile and run the code, and compare the results to a [saved copy of those from the ArXiV document](example.attacks/redo.korg.results.with.partial.order.reduction/).

The Dockerfile compiles a [special version of the code](example.attacks/redo.korg.results.with.partial.order.reduction/alternativeCharacterize.py) with [partial order reduction](https://spinroot.com/spin/Workshops/ws06/040.pdf) turned on.  This is an optimization in Spin which we used in the paper, but which we turn off in the default version of KORG in order to support models with rendezvous composition (i.e. size-0 [channels](https://spinroot.com/spin/Man/chan.html)).

````
sudo docker build -t korg .
````

If the Dockerfile fails to reproduce the exact results from the paper, it will also fail to build successfully (and will throw a warning in the terminal).

## How to use the tool.

See [`docs/Korg.md`](docs/Korg.md).
