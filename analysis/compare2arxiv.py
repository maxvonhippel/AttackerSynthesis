import glob

RES = "example.attacks/redo.korg.results.with.partial.order.reduction"

comparisons = [
	(RES + "/phi1.oldKorg.false_False", "out/experiment1_False_False"),
	(RES + "/phi1.oldKorg.true_True"  , "out/experiment1_True_True"  ),
	(RES + "/phi2.oldKorg.false_False", "out/experiment2_False_False"),
	(RES + "/phi2.oldKorg.true_True"  , "out/experiment2_True_True"  ),
	(RES + "/phi3.oldKorg.false_False", "out/experiment3_False_False"),
	(RES + "/phi3.oldKorg.true_True"  , "out/experiment3_True_True"  )
]

for (vAdir, vBdir) in comparisons:
	Aset = set()
	Bset = set()
	for vA in glob.glob(vAdir + "/*.pml"):
		with open(vA, "r") as fr:
			_ = next(fr)
			Aset.add(fr.read())
	for vB in glob.glob(vBdir + "/*.pml"):
		with open(vB, "r") as fr:
			_ = next(fr)
			Bset.add(fr.read())
	assert(Aset == Bset)

		