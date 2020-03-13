# ==============================================================================
# File      : test_Characterize.py
# Author    : Max von Hippel
# Authored  : 30 November 2019
# Purpose   : Tests Characterize.py
# How to run: $ make testChar
# ==============================================================================

import unittest
from Characterize import models

class TestCharacterize(unittest.TestCase):

	model = 'demo/TCP/TCP.pml'
	N     = 'demo/TCP/network.pml'
	D     = 'demo/TCP/daisy.pml'
	exp1  = 'experiments/experiment1.pml'
	exp2  = 'experiments/experiment2.pml'
	exp3  = 'experiments/experiment3.pml'

	def test_exp1(self):
		self.assertEqual(                             			    \
			models(self.model, self.exp1, self.N, "test_exp1.pml"), \
			True)

	def test_exp2(self):
		self.assertEqual(                          	  			    \
			models(self.model, self.exp2, self.N, "test_exp2.pml"), \
			True)

	def test_exp3(self):
		self.assertEqual( 							  			    \
			models(self.model, self.exp3, self.N, "test_exp3.pml"), \
			True)

	def test_violate_exp1(self):
		self.assertEqual(                             			    \
			models(self.model, self.exp1, self.D, "test_exp4.pml"), \
			False)

	def test_violate_exp2(self):
		self.assertEqual(                             		     	\
			models(self.model, self.exp2, self.D, "test_exp5.pml"), \
			False)