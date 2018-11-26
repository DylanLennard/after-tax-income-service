import unittest
import tax_app

class TestRawMethods(unittest.TestCase):

    INCOME = 50_000

    def test_fed_tax(self):
        fed_taxes = tax_app.federal_tax(TestRawMethods.INCOME)
        self.assertEqual(6_939.38, fed_taxes)

    def test_state_tax(self):
        state_taxes = tax_app.state_tax(TestRawMethods.INCOME)
        self.assertEqual(2_107.47, state_taxes)

    def test_other_tax(self):
        # test when status true
        other_taxes_status_true = tax_app.other_tax(TestRawMethods.INCOME, True)
        self.assertEqual(3_825.00, other_taxes_status_true)

        # test when status is False
        other_taxes_status_false = tax_app.other_tax(TestRawMethods.INCOME, False)
        self.assertEqual(7_650.00, other_taxes_status_false)

    def test_tax(self):
        tax = tax_app.tax(TestRawMethods.INCOME)
        self.assertEqual(37_128.15, tax)


if __name__ == '__main__':
    unittest.main()
