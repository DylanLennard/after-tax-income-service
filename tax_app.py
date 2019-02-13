# -*- coding: utf-8 -*-
'''
Takes input from user to calculate income tax before deductions.
'''

import json

TAX_DATA_FOLDER = "data/"
FEDERAL_TAX_FILE = TAX_DATA_FOLDER + 'federal_taxes.json'
STATE_TAX_FILE = TAX_DATA_FOLDER + 'state_taxes.json'


class Tax():
    """
    A Class to hold rate and bracket data for federal or state taxes
    This class will also be able to calculate the amount paid in taxes given 
    income as an input

    Args:
        * rates: the marginal tax rates themselves
        * brackets: the income brackets related to each rate (start at 0)
    """

    def __init__(self, rates: list, brackets: list):
        self.rates = rates
        self.brackets = brackets
        self.amount = 0

    def calculate(self, income: float) -> float:
        """
        Calculates the after tax income of a given form of taxes

        Args:
            income: float or int of the pre-tax income
        Returns:
            amount: the amount one has to pay for tax
        """
        for i, val in enumerate(self.brackets):
            if i == 0:  # may change this later if 0 not included in array
                continue
            if i == (len(self.brackets) - 1) and income > val:
                self.amount = self.amount + (income-val) * self.rates[i]
            elif income >= val:
                self.amount = self.amount + (val - self.brackets[i-1]) * self.rates[i-1]
            else:
                self.amount = self.amount + (income - self.brackets[i-1]) * self.rates[i-1]
                break

        return round(self.amount, 2)


def get_tax_info(income: float, state: str = 'CA') -> (Tax, Tax):
    """
    Constructs and returns the appropriate object of type Tax given inputs

    Arguments:
        income: the pretax income of an individual
        state: string of the state abbreviation
    """

    with open(FEDERAL_TAX_FILE, 'r') as f_fed, open(STATE_TAX_FILE, 'r') as f_state:
        fed_data = json.loads(f_fed.read())
        state_data = json.loads(f_state.read())

    fed_tax_obj = Tax(
        rates=fed_data['rates'],
        brackets=fed_data['brackets']
    )

    state_tax_obj = Tax(
        rates=state_data[state]['rates'],
        brackets=state_data[state]['brackets']
    )

    return fed_tax_obj, state_tax_obj


def other_tax(income: float, status: bool = True) -> float:
    '''
    Measures social security and medical based on employment.
    '''
    medicare_rate = 0.0145
    medicare_upper_rate = 0.0235  # for those making over $200000
    ssi_rate = 0.062  # up to $118,500

    # edit this and possibly the variable construction
    # also edit this to just look for y or n in stirng
    if not status:
        medicare_rate = medicare_rate * 2
        medicare_upper_rate = medicare_upper_rate * 2
        ssi_rate = ssi_rate * 2

    if income < 118_500:
        ssi_tax = income * ssi_rate
        medicare_tax = income * medicare_rate

    else:
        ssi_tax = 118_500 * ssi_rate
        if income <= 200_000:
            medicare_tax = income * medicare_rate
        else:
            medicare_tax = income * medicare_upper_rate

    total_other_tax = ssi_tax + medicare_tax
    return round(total_other_tax, 2)

