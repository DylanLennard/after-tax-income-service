import pytest
from tax_app import get_tax_info, other_tax

TEST_STATE = 'CA'
INCOME = 50_000
FED_INCOME_TAX = 6_939.38
STATE_INCOME_TAX = 2_107.47
OTHER_INCOME_TAX_NOT_SELF_EMP = 3_825.00
OTHER_INCOME_TAX_SELF_EMP = 7_650.00
TOTAL_EXPECTED_TAX = 37_128.15


def test_fed_tax():
    """Test that the federal tax function returns the correct value"""
    fed_tax, _ = get_tax_info(state="CA")
    fed_taxes_amt = fed_tax.calculate(INCOME)
    assert fed_taxes_amt == FED_INCOME_TAX


def test_state_tax():
    """Test that the state tax function returns correct value"""
    _, state_tax = get_tax_info(state="CA")
    state_taxes_amt = state_tax.calculate(INCOME)
    assert state_taxes_amt == STATE_INCOME_TAX


def test_other_tax_not_self_emp():
    """Test that other_tax function returns correct value if status==True"""
    other_taxes_status_true = other_tax(INCOME, False)
    assert other_taxes_status_true == OTHER_INCOME_TAX_NOT_SELF_EMP


def test_other_tax_self_emp():
    """Test that other_tax function returns correct value if status==False"""
    other_taxes_status_false = other_tax(INCOME, True)
    assert other_taxes_status_false == OTHER_INCOME_TAX_SELF_EMP


def test_tax():
    """Test that the main function as a whole works"""
    fed_tax, state_tax = get_tax_info(state=TEST_STATE)
    federal_amount = fed_tax.calculate(INCOME)
    state_amount = state_tax.calculate(INCOME)
    other_amount = other_tax(INCOME, status=False)

    tax = INCOME - federal_amount - state_amount - other_amount
    assert TOTAL_EXPECTED_TAX == tax
