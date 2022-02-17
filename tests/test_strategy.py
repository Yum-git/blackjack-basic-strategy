import unittest

from module.strategy import hard_strategy, soft_strategy, split_strategy


class TestStrategy(unittest.TestCase):
    def test_hard_case_1(self):
        """
        ハードストラテジーその1
        """
        choice_strategy = hard_strategy(13, 5)

        self.assertEqual(choice_strategy, "S")

    def test_hard_case_2(self):
        """
        ハードストラテジーその2
        """
        choice_strategy = hard_strategy(16, 1)

        self.assertEqual(choice_strategy, "R")

    def test_soft_case_1(self):
        """
        ソフトストラテジーその1
        """
        choice_strategy = soft_strategy(2, 9)

        self.assertEqual(choice_strategy, "H")

    def test_soft_case_2(self):
        """
        ソフトストラテジーその2
        """
        choice_strategy = soft_strategy(7, 6)

        self.assertEqual(choice_strategy, "D")

    def test_split_case_1(self):
        """
        スプリットストラテジーその1
        """
        choice_strategy = split_strategy(1, 11)

        self.assertEqual(choice_strategy, "P")

    def test_split_case_2(self):
        """
        スプリットストラテジーその2
        """
        choice_strategy = split_strategy(4, 8)

        self.assertEqual(choice_strategy, "H")