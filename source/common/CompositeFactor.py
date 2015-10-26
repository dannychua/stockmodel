__author__ = 'xiaofeng'

import Factor
import math
import pandas as pd
import numpy as np
from inspect import isfunction

class CompositeFactor(Factor):
    '''
    aggregate multiple factors to a composite factor, where a composite score is a linear weighed average of factor scores
    It handles static weights
    It is expected to handle dynamic weights where weight is a function of factor and stock
    '''

    def __init__(self, name, desc, factors, weights=None, univPP=None):
        '''
        initialize the composite factor by specifying the calculator
        :param factors: a list of Factor or CompositeFactor objects
        :param weights: could be None, a list of float, or a pd.Series of pd.DataFrame, where the index of Series is
        Date, and the index of DataFrame is StockID and the columns are factors.
        Each row represents an array of weights for a stock, and therefore its sum is equal to 1.0
        If it is None, then equal weights will be applied.
        If it is a list of float, it must have the same length as factors and the static weights will be applied.
        If it is a pd.Series, the dynamic weights will be applied
        :return: a composite factor object
        '''
        self.NumFactors = len(factors)
        self.Factors = factors
        if weights is None:
            weights = [1/self.NumFactors] * self.NumFactors       # equal weights
            self.Weights = weights
        elif type(weights) is list:
            if len(weights) != self.NumFactors:
                print "ERROR: the length of weights is NOT equal to the number of factors"
                exit(-1)

            noNegative = weights[weights > 0]
            if len(noNegative) > 0:
                print "ERROR: Negative weights"
                exit(-1)

            tot = math.fsum(weights)
            if math.fabs(tot - 1) > 0.01:
                print ("WARN: the sum of weights " + str(math.floor(tot,2)) + "is not equal to 1. ReWeight to 1.")
                weights = weights * 1.0 / tot

            self.Weights = weights
        elif type(weights) is pd.Series:
            pass  #todo dynamic weights, for backtest
        elif isfunction(weights):
            pass  #todo dynamic weights, for backtest & live trading, function arg is StockID,date,factorID
        else:
            print ("Unknown weights type: " + str(type(weights)))
            exit(-1)

        def myCalc(stockID, date):
            score = np.nan
            if type(self.Weights) is list:
                for i in range(self.NumFactors):
                    score += self.Weights[i] * self.Factors[i].GetScore(stockID, date)
            elif type(weights) is pd.Series:
                pass
            elif isfunction(weights):
                pass
            return score

        self.super(name, desc, myCalc, univPP)

