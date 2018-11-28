import unittest
import tax_app

class TestRawMethods(unittest.TestCase):

    INCOME = 50_000
    FED_INCOME_TAX = 6_939.38
    STATE_INCOME_TAX = 2_107.47
    OTHER_INCOME_TAX_NOT_SELF_EMP = 3_825.00
    OTHER_INCOME_TAX_SELF_EMP = 7_650.00
    TOTAL_EXPECTED_TAX = 37_128.15

    def test_fed_tax(self):
        """Test that the federal tax function returns the correct value"""
        fed_taxes = tax_app.federal_tax(TestRawMethods.INCOME)
        self.assertEqual(TestRawMethods.FED_INCOME_TAX, fed_taxes)

    def test_state_tax(self):
        """Test that the state tax function returns correct value"""
        state_taxes = tax_app.state_tax(TestRawMethods.INCOME)
        self.assertEqual(TestRawMethods.STATE_INCOME_TAX, state_taxes)

    def test_other_tax(self):
        """Test that other_tax function returns correct value given all parameters"""
        # test when status true
        other_taxes_status_true = tax_app.other_tax(TestRawMethods.INCOME, True)
        self.assertEqual(TestRawMethods.OTHER_INCOME_TAX_NOT_SELF_EMP, other_taxes_status_true)

        # test when status is False
        other_taxes_status_false = tax_app.other_tax(TestRawMethods.INCOME, False)
        self.assertEqual(TestRawMethods.OTHER_INCOME_TAX_SELF_EMP, other_taxes_status_false)

    def test_tax(self):
        """Test that the main function as a whole works"""
        tax = tax_app.tax(TestRawMethods.INCOME)
        self.assertEqual(TestRawMethods.TOTAL_EXPECTED_TAX, tax)


if __name__ == '__main__':
    unittest.main()
