import unittest
import tax_app

class TestRawMethods(unittest.TestCase):

    INCOME = 50_000

    def test_fed_tax(self):
        fed_taxes = tax_app.federal_tax(TestRawMethods.INCOME)
        self.assertEqual(8271.25, fed_taxes)

    def test_state_tax(self):
        state_taxes = tax_app.state_tax(TestRawMethods.INCOME)
        self.assertEqual(2212.50, state_taxes)

    def test_other_tax(self):
        # test when status true
        other_taxes_status_true = tax_app.other_tax(TestRawMethods.INCOME, True)
        self.assertEqual(3825.00, other_taxes_status_true)

        # test when status is False
        other_taxes_status_false = tax_app.other_tax(TestRawMethods.INCOME, False)
        self.assertEqual(7650.00, other_taxes_status_false)

    def test_tax(self):
        tax = tax_app.tax(TestRawMethods.INCOME)
        self.assertEqual(35691.25, tax)


if __name__ == '__main__':
    unittest.main()
