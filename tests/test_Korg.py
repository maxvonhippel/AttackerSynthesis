# ==============================================================================
# File      : test_Korg.py
# Author    : Max von Hippel and Cole Vick
# Authored  : 30 November 2019 - 13 March 2020
# Purpose   : Tests Korg.py
# How to run: $ make testKorg
# ==============================================================================

import unittest
import Korg

class TestKorg(unittest.TestCase):

	# Test on small toy problems
	P     = 'demo/livenessExample2/P.pml'
	Q     = 'demo/livenessExample2/Q.pml'
	phi   = 'demo/livenessExample2/wrongPhi.pml'
	psi   = 'demo/livenessExample2/phi.pml'
	theta = 'demo/livenessExample2/theta.pml'
	IO_P  = 'demo/livenessExample2/IO.txt'

	# Test on TCP model with 3 threat models
	TCP   = 'demo/TCP/TCP.pml'
	net   = 'demo/TCP/network.pml'
	IO    = 'demo/TCP/IO.txt'
	exp1  = 'experiments/experiment1.pml'
	exp2  = 'experiments/experiment2.pml'
	exp3  = 'experiments/experiment3.pml'
	
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
			_name = "test_errors_if_no_attackers_requested_" + str(_with_recovery)
			self.assertEqual(Korg.body( \
				model   = None,       \
				phi     = None,       \
				Q       = None,       \
				IO      = None,       \
				max_attacks = 0	, 	  \
				with_recovery  = _with_recovery,    \
				TESTING = True,       \
				name    = _name, \
				characterize = True), 1)
	
	# Test that if model || Q |/= phi then errors
	def test_errors_if_trivial(self):
		for _with_recovery in [ True, False ]:
			_name = "test_errors_if_trivial_" + str(_with_recovery)
			self.assertEqual(Korg.body(          \
					model   = self.P,          \
					phi     = self.phi,        \
					Q       = self.Q,          \
					IO      = None,            \
					max_attacks = self.maxAttacks, \
					with_recovery  = _with_recovery,         \
					TESTING = True,            \
					name = _name, \
					characterize = True), 3)
	
	# Test that if we cannot negate phi then we get back 2
	def test_errors_if_cannot_negate_phi(self):
		for _with_recovery in [ True, False ]:
			_name = "test_errors_if_cannot_negate_phi_" + str(_with_recovery)
			self.assertEqual(Korg.body(      \
				model   = None,            \
				phi     = None,            \
				Q       = None,            \
				IO      = None,            \
				max_attacks = self.maxAttacks, \
				with_recovery  = _with_recovery,         \
				TESTING = True,            \
				name    = _name, \
				characterize = True), 2)

	# Test that if IO is empty then we error, get back 4 or 5
	def test_errors_if_IO_None(self):
		for _with_recovery in [ True, False ]:
			for _IO in [ None, 'dne.blarg', 'demo/emptyFile' ]:
				_name = "test_errors_if_IO_None_" \
					  + str(_with_recovery)              \
					  + "_"                       \
					  + str(_IO).replace("demo/", "")
				_exp  = 4 if _IO == None else 5
				self.assertEqual(Korg.body(      \
					model   = self.TCP,        \
					phi     = self.exp1,       \
					Q       = self.net,        \
					IO      = _IO,             \
					max_attacks     = self.maxAttacks, \
					with_recovery  = _with_recovery,         \
					TESTING = True,            \
					name    = _name, \
					characterize = True), _exp)

	# Test that if cannot make daisy then we error, get back 6
	# Also test that if no solution exists, ie, daisy doesn't violate,
	# then we error, get back 6
	def test_errors_if_no_solution(self):
		for _with_recovery in [ True, False ]:
			_name = "test_errors_if_no_solution_" + str(_with_recovery)
			self.assertEqual(Korg.body(      \
				model   = self.P,          \
				phi     = self.theta,      \
				Q       = self.Q,          \
				IO      = self.IO_P,       \
				max_attacks     = self.maxAttacks, \
				with_recovery  = _with_recovery,         \
				TESTING = True,            \
				name    = _name, \
				characterize = True), 6)
	
	def test_works_on_TCP_exp1_with_recovery(self):
		self.assertEqual(Korg.body(      \
			model   = self.TCP,        \
			phi     = self.exp1,       \
			Q       = self.net,        \
			IO      = self.IO,         \
			max_attacks     = self.maxAttacks, \
			with_recovery  = True,    	       \
			TESTING = True,            \
			name    = "test_works_on_TCP_exp1_with_recovery", \
			characterize = True), 0)

	def test_works_on_TCP_exp1_not_with_recovery(self):
		self.assertEqual(Korg.body(      \
			model   = self.TCP,        \
			phi     = self.exp1,       \
			Q       = self.net,        \
			IO      = self.IO,         \
			max_attacks     = self.maxAttacks, \
			with_recovery  = False,           \
			TESTING = True,            \
			name    = "test_works_on_TCP_exp1_not_with_recovery", \
			characterize = True), 0)
	
	def test_works_on_TCP_exp2_with_recovery(self):
		self.assertEqual(Korg.body(      \
			model   = self.TCP,        \
			phi     = self.exp2,       \
			Q       = self.net,        \
			IO      = self.IO,         \
			max_attacks     = self.maxAttacks, \
			with_recovery  = True,    	       \
			TESTING = True,            \
			name    = "test_works_on_TCP_exp2_with_recovery", \
			characterize = True), 0)

	def test_works_on_TCP_exp2_not_with_recovery(self):
		self.assertEqual(Korg.body(      \
			model   = self.TCP,        \
			phi     = self.exp2,       \
			Q       = self.net,        \
			IO      = self.IO,         \
			max_attacks     = self.maxAttacks, \
			with_recovery  = False,           \
			TESTING = True,            \
			name    = "test_works_on_TCP_exp2_not_with_recovery", \
			characterize = True), 0)

	def test_fails_on_with_recovery_Liveness(self):
		self.assertEqual(Korg.body(                     \
			model   = self.s_P,   \
			phi     = self.s_Phi, \
			Q       = self.s_Q,   \
			IO      = self.s_IO,  \
			max_attacks = self.maxAttacks,                \
			with_recovery  = True,                           \
			TESTING = True,							  \
			name    = "test_fails_on_with_recovery_Liveness", \
			characterize = True), 6)

	def test_works_on_non_with_recovery_Liveness(self):
		self.assertEqual(Korg.body(                     \
			model   = self.s_P,   \
			phi     = self.s_Phi, \
			Q       = self.s_Q,   \
			IO      = self.s_IO,  \
			max_attacks = self.maxAttacks,            \
			with_recovery  = False,                          \
			TESTING = True,                           \
			name    = "test_works_on_non_with_recovery_Liveness", \
			characterize = True), 0)

	def test_works_on_Coles_example_with_recovery(self):
		self.assertEqual(Korg.body(      \
			model   = self.s_P,        \
			phi     = self.s_Phi,      \
			Q       = self.s_Q,        \
			IO      = self.s_IO,       \
			max_attacks     = self.maxAttacks, \
			with_recovery  = True,            \
			TESTING = True,            \
			name    = "test_works_on_Coles_example_with_recovery", \
			characterize = True), 6)

	def test_works_on_Coles_example_non_with_recovery(self):
		self.assertEqual(Korg.body(      \
			model   = self.s_P,        \
			phi     = self.s_Phi,      \
			Q       = self.s_Q,        \
			IO      = self.s_IO,       \
			max_attacks     = self.maxAttacks, \
			with_recovery  = False,           \
			TESTING = True,            \
			name    = "test_works_on_Coles_example_non_with_recovery", \
			characterize = True), 0)
