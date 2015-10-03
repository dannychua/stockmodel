""" 
Build factor score cache for all factors 
"""

import os
import sys
import cPickle as pickle
import common.GlobalConstant as GlobalConstant
from common.Factor import Factor
from common.PortfolioProviders import PortfolioProviders



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
        # Decode pickled objects
        f = file(a50ppCachePath, 'rb')
        a50PP = pickle.load(f)
        f = file(zz800ppCachePath, 'rb')
        zz800PP = pickle.load(f)

    # Build cache if not exist
    else:
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


buildFactorCache()