import unittest
from ragbench.core import *

class EvaluationTests(unittest.TestCase):
    def test_multiset_overlap(self):
        self.assertAlmostEqual(token_f1('a a b', 'a b b'), 2 / 3)
        self.assertEqual(token_f1('', ''), 1)

    def test_retrieval_cutoff(self):
        self.assertEqual(ranking_metrics(['x', 'r'], ['r'], 1)['recall'], 0)
        self.assertEqual(ranking_metrics(['x', 'r'], ['r'], 2)['mrr'], .5)
