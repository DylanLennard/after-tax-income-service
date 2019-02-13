# -*- coding: utf-8 -*-
'''
Takes input from user to calculate income tax before deductions.
'''


class Tax():

    def __init__(self, rates: list, bracket: list, income: float):
        self.income = income
        self.rates = rates
        self.bracket = bracket
        self.amount = 0

    def calculate(self) -> float:
        """
        Calculates the after tax income of a given form of taxes

        Args:
            income: float or int of the pre-tax income
        Returns:
            amount: the amount one has to pay for tax
        """
        # TODO: consider redoing this
        for i, val in enumerate(self.bracket):
            if i == 0:  # may change this later if 0 not included in array
                continue
            if i == (len(self.bracket) - 1) and self.income > val:
                self.amount = self.amount + (self.income-val) * self.rates[i]
            elif self.income >= val:
                self.amount = self.amount + (val - self.bracket[i-1]) * self.rates[i-1]
            else:
                self.amount = self.amount + (self.income - self.bracket[i-1]) * self.rates[i-1]
                break

        return round(self.amount, 2)


def state_tax(income: float) -> float:
    '''
    Go http://www.tax-brackets.org/ and store data in json
    State should be key to a 2-d array. Or query as needed
    and just store in array, probably the latter is best
    '''
    rates = [0.01, 0.02, 0.04, 0.06, 0.08, 0.093,
             0.103, 0.113, 0.123, 0.133]
    brackets = [0, 8_015, 19_001, 29_989, 41_629, 52_612, 268_750,
                322_499, 537_498, 1_000_000]
    state = 'CA'  # Can just add attributes to class as you go as well.

    state = Tax(rates, brackets, income)

    return state.calculate()


def federal_tax(income: float) -> float:
    '''
    http://taxfoundation.org/article/2016-tax-brackets
    and store in array or in dataframe
    '''
    rates = [0.1, 0.12, 0.22, 0.24, 0.32, 0.35, 0.37]
    brackets = [0, 9_526, 38_701, 82_501, 157_501, 200_001, 500_001]

    fed = Tax(rates, brackets, income)

    return fed.calculate()


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
    return total_other_tax


def tax(income: float, status: bool = True) -> float:
    """Calculate the actual tax"""
    if status is None: status = True
    federal_amount = federal_tax(income)
    state_amount = state_tax(income)
    other_amount = other_tax(income, status)

    after_tax = income - federal_amount - state_amount - other_amount

    return after_tax
