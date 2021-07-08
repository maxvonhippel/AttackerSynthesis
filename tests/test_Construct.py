# ==============================================================================
# File      : test_Construct.py
# Author    : Cole Vick
# Authored  : Sometime in February 2020
# Purpose   : Tests Construct.py
# How to run: $ make testCons
# ==============================================================================

import unittest
from korg import Construct as c
from korg.CLI import cleanUpAlias

class TestConstruct(unittest.TestCase):

    s_Q   = 'demo/livenessExample1/Q.pml'
    s_P   = 'demo/livenessExample1/P.pml'
    s_IO  = 'demo/livenessExample1/IO.txt'
    s_Phi = 'demo/livenessExample1/Phi.pml'
    IO    = sorted(list(c.getIO(s_IO)))

    s_network, s_label = c.makeDaisy(IO,s_Q)

    # Checks that bit for recovery logic was set correctly
    def test_makeDaisy1(self):
        self.assertEqual(self.s_label, "b")

    # Tests that daisy in a particular example was made correctly
    def test_makeDaisyWithEvent(self):
        daisyBod = 'active proctype daisy () {\n\tdo\n\t:: channel!C;'
        daisyBod += '\n\t:: channel?A;\n\t:: channel?B;\n\tod\n}'
        daisy_string = c.makeDaisyWithEvents(
            self.IO, False, self.s_network, self.s_label)
        self.assertEqual(daisy_string, daisyBod)

    # Same but for recovery case
    def test_makeDaisyPhiFinite(self):
        d_phi = " ".join([b for b in                              \
                    [a.strip() for a in                           \
                    c.makeDaisyPhiFinite(self.s_label, self.s_Phi)\
                     .replace("\n", "")                           \
                     .replace("\t", " ")                          \
                     .split(" ")] if len(b) > 0])

        daisyBod = "ltl newPhi { (eventually ( b == 1 ) ) implies ( eventually"
        daisyBod += " ( always ( w == 0 ) ) )}"
        self.assertEqual(d_phi, daisyBod)

    @classmethod
    def tearDownClass(cls):
        cleanUpAlias()
