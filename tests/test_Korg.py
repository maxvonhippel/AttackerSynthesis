# ==============================================================================
# File      : test_Korg.py
# Author    : Max von Hippel and Cole Vick
# Authored  : 30 November 2019 - 13 March 2020
# Purpose   : Tests Korg.py
# How to run: $ make testKorg
# ==============================================================================

import unittest
from korg import Korg
from korg.CLI import cleanUpAlias

class TestKorg(unittest.TestCase):

	# Test on small toy problems
	P     = 'demo/livenessExample2/P.pml'
	Q     = 'demo/livenessExample2/Q.pml'
	phi   = 'demo/livenessExample2/wrongPhi.pml'
	psi   = 'demo/livenessExample2/phi.pml'
	theta = 'demo/livenessExample2/theta.pml'
	IO_P  = 'demo/livenessExample2/IO.txt'

	# Test on TCP model with 3 threat models
	TCP   = 'demo/TCP.korg/TCP.pml'
	net   = 'demo/TCP.korg/network.pml'
	IO    = 'demo/TCP.korg/IO.txt'
	exp1  = 'demo/TCP.korg/phi1.pml'
	exp2  = 'demo/TCP.korg/phi2.pml'
	exp3  = 'demo/TCP.korg/phi3.pml'
	
	# Test Cole's experiments
	s_P   = 'demo/livenessExample1/P.pml'
	s_Q   = 'demo/livenessExample1/Q.pml'
	s_IO  = 'demo/livenessExample1/IO.txt'
	s_Phi = 'demo/livenessExample1/Phi.pml' 

	maxAttacks = 1

	# In below tests we invoke the following function from Generator3:
	# body(model, phi, Q, IO, max_attacks, with_recovery, TESTING=False)

	# Test that if max_attacks < 1 we get back error code 1
	def test_errors_if_no_attackers_requested(self):
		for _with_recovery in [ True, False ]:
			_name = "test_errors_if_no_attackers_requested_" 
			_name += str(_with_recovery)
			self.assertEqual(Korg.body(                        \
				model = None, phi = None, Q = None, IO = None, \
				max_attacks   = 0, 	                           \
				with_recovery = _with_recovery,                \
				name          = _name,                         \
				characterize  = True), 1)
	
	# Test that if model || Q |/= phi then errors
	def test_errors_if_trivial(self):
		for _with_recovery in [ True, False ]:
			_name = "test_errors_if_trivial_" + str(_with_recovery)
			self.assertEqual(Korg.body(              \
					model         = self.P,          \
					phi           = self.phi,        \
					Q             = self.Q,          \
					IO            = None,            \
					max_attacks   = self.maxAttacks, \
					with_recovery = _with_recovery,  \
					name          = _name,           \
					characterize  = True), 3)
	
	# Test that if we cannot negate phi then we get back 2
	def test_errors_if_cannot_negate_phi(self):
		for _with_recovery in [ True, False ]:
			_name = "test_errors_if_cannot_negate_phi_" + str(_with_recovery)
			self.assertEqual(Korg.body(                        \
				model = None, phi = None, Q = None, IO = None, \
				max_attacks   = self.maxAttacks,               \
				with_recovery = _with_recovery,                \
				name          = _name,                         \
				characterize  = True), 2)

	# Test that if IO is empty then we error, get back 4 or 5
	def test_errors_if_IO_None(self):
		for _with_recovery in [ True, False ]:
			for _IO in [ None, 'dne.blarg', 'demo/emptyFile' ]:
				_name = "test_errors_if_IO_None_" + str(_with_recovery) \
					  + "_" + str(_IO).replace("demo/", "")
				_exp  = 4 if _IO == None else 5
				self.assertEqual(Korg.body(          \
					model         = self.TCP,        \
					phi           = self.exp1,       \
					Q             = self.net,        \
					IO            = _IO,             \
					max_attacks   = self.maxAttacks, \
					with_recovery = _with_recovery,  \
					name          = _name,           \
					characterize  = True), _exp)

	# Test that if cannot make daisy then we error, get back 6
	# Also test that if no solution exists, ie, daisy doesn't violate,
	# then we error, get back 6
	def test_errors_if_no_solution(self):
		for _with_recovery in [ True, False ]:
			_name = "test_errors_if_no_solution_" + str(_with_recovery)
			self.assertEqual(Korg.body(           \
				model          = self.P,          \
				phi            = self.theta,      \
				Q              = self.Q,          \
				IO             = self.IO_P,       \
				max_attacks    = self.maxAttacks, \
				with_recovery  = _with_recovery,  \
				name           = _name,           \
				characterize = True), 6)
	
	# Test that we can find attackers for experiment_1 with and without recovery
	def test_works_on_TCP_exp1(self):
		for _recovery in [ True, False ]:
			self.assertEqual(Korg.body(           \
				model          = self.TCP,        \
				phi            = self.exp1,       \
				Q              = self.net,        \
				IO             = self.IO,         \
				max_attacks    = self.maxAttacks, \
				with_recovery  = _recovery,    	  \
				name = "test_works_on_TCP_exp1_" + str(_recovery), \
				characterize   = True), 0)
	
	# Test that we can find attackers for experiment_2 with and without recovery
	def test_works_on_TCP_exp2(self):
		for _recovery in [ True, False ]:
			self.assertEqual(Korg.body(           \
				model          = self.TCP,        \
				phi            = self.exp2,       \
				Q              = self.net,        \
				IO             = self.IO,         \
				max_attacks    = self.maxAttacks, \
				with_recovery  = _recovery,    	  \
				name           = "test_works_on_TCP_exp2_" + str(_recovery), \
				characterize   = True), 0)

	# We don't test exp3 because it takes too long, but we encourage you to
	# try it out if you're curious!  See the documentation and Makefile for 
	# more.

	# Now let's try a toy problem where we can solve w/out recovery but not w/.
	def test_on_Liveness(self):
		for _recovery in [ True, False ]:
			self.assertEqual(Korg.body(          \
				model         = self.s_P,        \
				phi           = self.s_Phi,      \
				Q             = self.s_Q,        \
				IO            = self.s_IO,       \
				max_attacks   = self.maxAttacks, \
				with_recovery = _recovery,       \
				name          = "test_"          \
							  + ("fails" if _recovery else "works") \
							  + "_on_Liveness_" + str(_recovery),   \
				characterize  = True), 6 if _recovery else 0)

	# Opposite logic to prior test.
	def test_works_on_Coles_example(self):
		for _recovery in [ True, False ]:
			self.assertEqual(Korg.body(          \
				model         = self.s_P,        \
				phi           = self.s_Phi,      \
				Q             = self.s_Q,        \
				IO            = self.s_IO,       \
				max_attacks   = self.maxAttacks, \
				with_recovery = _recovery,       \
				name          = "test_works_on_Coles_example_" \
							  + str(_recovery),  \
				characterize  = True), 6 if _recovery else 0)

	@classmethod
	def tearDownClass(cls):
		cleanUpAlias()
