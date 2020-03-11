import unittest
import Gen3 as g3

class TestGen3(unittest.TestCase):

	P     = 'demo/LivenessExample/P.pml'
	Q     = 'demo/LivenessExample/Q.pml'
	phi   = 'demo/LivenessExample/wrongPhi.pml'
	psi   = 'demo/LivenessExample/phi.pml'
	theta = 'demo/LivenessExample/theta.pml'
	IO_P  = 'demo/LivenessExample/IO.txt'
	TCP   = 'demo/TCP/TCP.pml'
	net   = 'demo/TCP/network.pml'
	IO    = 'demo/TCP/IO.txt'
	exp1  = 'experiments/experiment1.pml'
	exp2  = 'experiments/experiment2.pml'
	exp3  = 'experiments/experiment3.pml'
	# Test Cole's experiments
	s_P   = 'demo/Cole/smallDemo1/P.pml'
	s_Q   = 'demo/Cole/smallDemo1/Q.pml'
	s_IO  = 'demo/Cole/smallDemo1/IO.txt'
	s_Phi = 'demo/Cole/smallDemo1/Phi.pml' 

	maxAttacks = 1

	# In below tests we invoke the following function from Generator3:
	# body(model, phi, Q, IO, max_attacks, finite, TESTING=False)

	# Test that if max_attacks < 1 we get back error code 1
	def test_errors_if_no_attackers_requested(self):
		for _finite in [ True, False ]:
			_name = "test_errors_if_no_attackers_requested_" + str(_finite)
			self.assertEqual(g3.body( \
				model   = None,       \
				phi     = None,       \
				Q       = None,       \
				IO      = None,       \
				max_attacks = 0	, 	  \
				finite  = _finite,    \
				TESTING = True,       \
				name    = _name, \
				characterize = True), 1)
	
	# Test that if model || Q |/= phi then errors
	def test_errors_if_trivial(self):
		for _finite in [ True, False ]:
			_name = "test_errors_if_trivial_" + str(_finite)
			self.assertEqual(g3.body(          \
					model   = self.P,          \
					phi     = self.phi,        \
					Q       = self.Q,          \
					IO      = None,            \
					max_attacks = self.maxAttacks, \
					finite  = _finite,         \
					TESTING = True,            \
					name = _name, \
					characterize = True), 3)
	
	# Test that if we cannot negate phi then we get back 2
	def test_errors_if_cannot_negate_phi(self):
		for _finite in [ True, False ]:
			_name = "test_errors_if_cannot_negate_phi_" + str(_finite)
			self.assertEqual(g3.body(      \
				model   = None,            \
				phi     = None,            \
				Q       = None,            \
				IO      = None,            \
				max_attacks = self.maxAttacks, \
				finite  = _finite,         \
				TESTING = True,            \
				name    = _name, \
				characterize = True), 2)

	# Test that if IO is empty then we error, get back 4 or 5
	def test_errors_if_IO_None(self):
		for _finite in [ True, False ]:
			for _IO in [ None, 'dne.blarg', 'demo/emptyFile' ]:
				_name = "test_errors_if_IO_None_" + str(_finite) + "_" + str(_IO).replace("demo/", "")
				_exp  = 4 if _IO == None else 5
				self.assertEqual(g3.body(      \
					model   = self.TCP,        \
					phi     = self.exp1,       \
					Q       = self.net,        \
					IO      = _IO,             \
					max_attacks     = self.maxAttacks, \
					finite  = _finite,         \
					TESTING = True,            \
					name    = _name, \
					characterize = True), _exp)

	# Test that if cannot make daisy then we error, get back 6
	# Also test that if no solution exists, ie, daisy doesn't violate,
	# then we error, get back 6
	def test_errors_if_no_solution(self):
		for _finite in [ True, False ]:
			_name = "test_errors_if_no_solution_" + str(_finite)
			self.assertEqual(g3.body(      \
				model   = self.P,          \
				phi     = self.theta,      \
				Q       = self.Q,          \
				IO      = self.IO_P,       \
				max_attacks     = self.maxAttacks, \
				finite  = _finite,         \
				TESTING = True,            \
				name    = _name, \
				characterize = True), 6)
	
	# WORKS
	def test_works_on_TCP_exp1_finite(self):
		self.assertEqual(g3.body(      \
			model   = self.TCP,        \
			phi     = self.exp1,       \
			Q       = self.net,        \
			IO      = self.IO,         \
			max_attacks     = self.maxAttacks, \
			finite  = True,    	       \
			TESTING = True,            \
			name    = "test_works_on_TCP_exp1_finite", \
			characterize = True), 0)

	# WORKS
	def test_works_on_TCP_exp1_not_finite(self):
		self.assertEqual(g3.body(      \
			model   = self.TCP,        \
			phi     = self.exp1,       \
			Q       = self.net,        \
			IO      = self.IO,         \
			max_attacks     = self.maxAttacks, \
			finite  = False,           \
			TESTING = True,            \
			name    = "test_works_on_TCP_exp1_not_finite", \
			characterize = True), 0)
	
	# WORKS
	def test_works_on_TCP_exp2_finite(self):
		self.assertEqual(g3.body(      \
			model   = self.TCP,        \
			phi     = self.exp2,       \
			Q       = self.net,        \
			IO      = self.IO,         \
			max_attacks     = self.maxAttacks, \
			finite  = True,    	       \
			TESTING = True,            \
			name    = "test_works_on_TCP_exp2_finite", \
			characterize = True), 0)

	# WORKS
	def test_works_on_TCP_exp2_not_finite(self):
		self.assertEqual(g3.body(      \
			model   = self.TCP,        \
			phi     = self.exp2,       \
			Q       = self.net,        \
			IO      = self.IO,         \
			max_attacks     = self.maxAttacks, \
			finite  = False,           \
			TESTING = True,            \
			name    = "test_works_on_TCP_exp2_not_finite", \
			characterize = True), 0)

	# FAILS
	def test_fails_on_finite_Liveness(self):
		self.assertEqual(g3.body(                     \
			model   = 'demo/LivenessExample/P.pml',   \
			phi     = 'demo/LivenessExample/phi.pml', \
			Q       = 'demo/LivenessExample/Q.pml',   \
			IO      = 'demo/LivenessExample/IO.txt',  \
			max_attacks     = self.maxAttacks,                \
			finite  = True,                           \
			TESTING = True,							  \
			name    = "test_fails_on_finite_Liveness", \
			characterize = True), -1)

	# WORKS
	def test_works_on_non_finite_Liveness(self):
		self.assertEqual(g3.body(                     \
			model   = 'demo/LivenessExample/P.pml',   \
			phi     = 'demo/LivenessExample/phi.pml', \
			Q       = 'demo/LivenessExample/Q.pml',   \
			IO      = 'demo/LivenessExample/IO.txt',  \
			max_attacks = self.maxAttacks,            \
			finite  = False,                          \
			TESTING = True,                           \
			name    = "test_works_on_non_finite_Liveness", \
			characterize = True), 0)

	# WORKS
	def test_works_on_Coles_example_finite(self):
		self.assertEqual(g3.body(      \
			model   = self.s_P,        \
			phi     = self.s_Phi,      \
			Q       = self.s_Q,        \
			IO      = self.s_IO,       \
			max_attacks     = self.maxAttacks, \
			finite  = True,            \
			TESTING = True,            \
			name    = "test_works_on_Coles_example_finite", \
			characterize = True), 6)

	# WORKS
	def test_works_on_Coles_example_non_finite(self):
		self.assertEqual(g3.body(      \
			model   = self.s_P,        \
			phi     = self.s_Phi,      \
			Q       = self.s_Q,        \
			IO      = self.s_IO,       \
			max_attacks     = self.maxAttacks, \
			finite  = False,           \
			TESTING = True,            \
			name    = "test_works_on_Coles_example_non_finite", \
			characterize = True), 0)
