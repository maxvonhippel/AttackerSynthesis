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

	print("Comparing " + vAdir + " to " + vBdir)

	Aset = set()
	Bset = set()

	Aset2f = { }
	Bset2f = { }

	for vA in glob.glob(vAdir + "/*.pml"):
		with open(vA, "r") as fr:
			_ = next(fr)
			txt = fr.read()
			Aset.add(txt)
			Aset2f[txt] = vA
	
	for vB in glob.glob(vBdir + "/*.pml"):
		with open(vB, "r") as fr:
			_ = next(fr)
			txt = fr.read()
			Bset.add(txt)
			Bset2f[txt] = vB
	
	assert(Aset == Bset)
	assert(len(Aset) == len(Bset))

	for a in Aset:
		assert(a in Bset)
		print(Aset2f[a] + " == " + Bset2f[a])



		