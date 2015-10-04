""" 
Build factor score cache for all factors 
"""

import os
import sys
from datetime import datetime
import cPickle as pickle
import common.GlobalConstant as GlobalConstant
from common.Factor import Factor
from common.PortfolioProviders import PortfolioProviders
import common.QDate as QDate
from common.Factor import Factor
import common.Factorlib.BPCalc as BPCalc



def buildFactorCache():
    """ Build factor score cache for all factors """

    # Avoid error `maximum recursion depth exceeded`
    sys.setrecursionlimit(1000)

    # Retrieve all PortfolioProviders
    a50PP, zz800PP = getAllPP()



def getAllPP():
    """ Retrieve all PortfolioProviders 
        Hits flatfile cache first, before querying database
    """
    # Construct path to cache file
    universesPath = os.path.join(GlobalConstant.DATA_DIR, 'Universes')
    a50ppCachePath = os.path.join(universesPath, 'a50PP.dat')
    zz800ppCachePath = os.path.join(universesPath, 'zz800PP.dat')

    # Load cache if cache file exist
    if os.path.isfile(a50ppCachePath) & os.path.isfile(zz800ppCachePath):
        a50PP, zz800PP = getAllPPFromCache()
    # Build cache if not exist
    else:
        a50PP, zz800PP = getAllPPFromDb()

    return (a50PP, zz800PP)


def getAllPPFromCache():
    """ Retrieve all PortfolioProviders from flat file cache """
    # Construct path to cache file
    universesPath = os.path.join(GlobalConstant.DATA_DIR, 'Universes')
    a50ppCachePath = os.path.join(universesPath, 'a50PP.dat')
    zz800ppCachePath = os.path.join(universesPath, 'zz800PP.dat')

    # Decode pickled objects
    f = file(a50ppCachePath, 'rb')
    a50PP = pickle.load(f)
    f = file(zz800ppCachePath, 'rb')
    zz800PP = pickle.load(f)

    return (a50PP, zz800PP)


def getAllPPFromDb():
    """ Retrieve all PortfolioProviders from Databases """
    
    # Construct path to cache file
    universesPath = os.path.join(GlobalConstant.DATA_DIR, 'Universes')
    a50ppCachePath = os.path.join(universesPath, 'a50PP.dat')
    zz800ppCachePath = os.path.join(universesPath, 'zz800PP.dat')

    # Grab data
    a50PP = PortfolioProviders.getA50()
    zz800PP = PortfolioProviders.getZhongZheng800()

    # Write data to disk
    if not os.path.exists(universesPath):
        os.makedirs(universesPath)
    with open(a50ppCachePath, 'w') as fp:
        pickle.dump(a50PP, fp)
    with open(zz800ppCachePath, 'w') as fp:
        pickle.dump(zz800PP, fp)

    return (a50PP, zz800PP)


# # Build Factor cache
buildFactorCache()

# Setup datetimes
WeekDts = QDate.WeekEndsBtw( datetime.strptime('20090401', '%Y%m%d'), datetime.strptime('20141231', '%Y%m%d') )
MonthDts = QDate.MonthEndsBtw( datetime.strptime('20090401', '%Y%m%d'), datetime.strptime('20141231', '%Y%m%d') )
CacheDts = QDate.UnionDistinct(WeekDts, MonthDts)


#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# Bugs in imported modules, unable to continue
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# Setup PortfolioProviders
a50PP, zz800PP = getAllPP()
BP = Factor('BP', 'Book/Price', BPCalc, zz800PP)
zBP = BP.Z(False, zz800PP)
zBP_SN = BP.Z(True, zz800PP)

# Calculate Scores and Save
BP.CalcScoresAndSave(CacheDts, zz800PP)
zBP.CalcScoresAndSave(CacheDts, zz800PP)
zBP_SN.CalcScoresAndSave(CacheDts, zz800PP)