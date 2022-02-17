import unittest

from module.count import card_list_count


class TestCount(unittest.TestCase):
    def test_case_1(self):
        """
        通常の足し算
        """
        card_count = card_list_count([2, 3, 4])

        self.assertEqual(card_count, 9)

    def test_case_2(self):
        """
        絵札が絡んだ足し算
        """

        card_count = card_list_count([2, 5, 12])

        self.assertEqual(card_count, 17)

    def test_case_3(self):
        """
        Aが絡んだ足し算
        """
        card_count = card_list_count([1, 2, 3])

        self.assertEqual(card_count, 16)

    def test_case_4(self):
        """
        Aが2枚絡んだ足し算
        """
        card_count = card_list_count([1, 1, 2])

        self.assertEqual(card_count, 14)

    def test_case_5(self):
        """
        Aが絡んで且つ全てのAが1の扱いになっている足し算
        """
        card_count = card_list_count([1, 1, 1, 3, 4, 11])

        self.assertEqual(card_count, 20)
