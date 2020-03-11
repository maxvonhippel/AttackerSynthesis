import unittest
import Construct as c


class TestConstruct(unittest.TestCase):

    s_Q   = 'demo/Cole/smallDemo1/Q.pml'
    s_P   = 'demo/Cole/smallDemo1/P.pml'
    s_IO  = 'demo/Cole/smallDemo1/IO.txt'
    s_Phi = 'demo/Cole/smallDemo1/Phi.pml'
    IO    = sorted(list(c.getIO(s_IO))) # make this list testable, it already is sorted in G3

    s_network, s_label = c.makeDaisy(IO,s_Q)

    def test_makeDaisy1(self): # need an example that is not trivial
        self.assertEqual(self.s_label, "b") # TODO: I don't see a single `bit b` in any network model. Is this needed?

    def test_makeDaisyWithEvent(self):
        daisy_string = c.makeDaisyWithEvents(self.IO, False, self.s_network, self.s_label)
        self.assertEqual(daisy_string, 'active proctype daisy () {\n\tdo\n\t:: channel!C;\n\t:: channel?A;\n\t:: channel?B;\n\tod\n}')

    def test_makeDaisyPhiFinite(self):
        d_phi = c.makeDaisyPhiFinite(self.s_label, self.s_Phi)
        self.assertEqual(d_phi, "ltl newPhi {\n\talways ( ( b == 1 ) implies\n\t\t\n\teventually always ( w == 0 )\n )\n}")
