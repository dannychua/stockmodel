""" 
Build factor score cache for all factors 
"""

import os
from datetime import datetime
import cPickle as pickle

import common.GlobalConstant as GlobalConstant
from common.PortfolioProviders import PortfolioProviders
import common.QDate as QDate
from common.Factor import Factor
from common.Factorlib.WINDIndicators import *
from common.TileAnalysis import TileAnalysis


# if the database is on local pc, it may be faster to load it from db than from files  by xxia on 10/10/2015
def getAllPP():
    """ Retrieve all PortfolioProviders 
        Hits flatfile cache first, before querying database
    """
    # Construct path to cache file
    #universesPath = os.path.join(GlobalConstant.DATA_DIR, 'Universes')
    universesPath = GlobalConstant.DATA_Universes_DIR
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
    f = file(a50ppCachePath, 'r')
    a50PP = pickle.load(f)
    f = file(zz800ppCachePath, 'r')
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


# Setup datetimes
SatDts = QDate.SaturdayBtw(datetime.strptime('20090401', '%Y%m%d'), datetime.strptime('20141231', '%Y%m%d') )
MonthDts = QDate.MonthEndsBtw(datetime.strptime('20090401', '%Y%m%d'), datetime.strptime('20141231', '%Y%m%d') )
CacheDts = SatDts.union(MonthDts)


#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# Bugs in imported modules, unable to continue
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# Setup PortfolioProviders
a50PP, zz800PP =  getAllPPFromCache() # getAllPPFromDb() #getAllPP()
# BP_a50PP = Factor('BP', 'Book/Price', BPCalc, a50PP)
BP_zz800PP = Factor('BP', 'Book/Price', BPCalc, zz800PP)
EP_zz800PP = Factor('EP', 'Earnings/Price', EPCalc, zz800PP)
EPttm_zz800PP = Factor('EPttm', 'TTM Earnings/Price', EPttmCalc, zz800PP)
CFP_zz800PP = Factor('CFP', 'Net Cash flow/Price', CFPCalc, zz800PP)
CFPttm_zz800PP = Factor('CFPttm', 'TTM Net Cash flow/Price', CFPttmCalc, zz800PP)
OCFP_zz800PP = Factor('OCFP', 'Operating Cash flow/Price', OCFPCalc, zz800PP)
OCFPttm_zz800PP = Factor('OCFPttm', 'TTM Operating Cash flow/Price', OCFPttmCalc, zz800PP)
SalesP_zz800PP = Factor('SalesP', 'Sales/Price', SalesPCalc, zz800PP)
SalesPttm_zz800PP = Factor('SalesPttm', 'TTM Sales/Price', SalesPttmCalc, zz800PP)
Turnover_zz800PP = Factor('Turnover', 'Turnover', TurnoverCalc, zz800PP)
FreeTurnover_zz800PP = Factor('FreeTurnover', 'Free Turnover', TurnoverCalc, zz800PP)
DividendYield_zz800PP = Factor('DividendYield', 'Dividend Yield', DividendYieldCalc, zz800PP)

factors = []
factors.append(BP_zz800PP)
factors.append(EP_zz800PP)
factors.append(EPttm_zz800PP)
factors.append(CFP_zz800PP)
factors.append(CFPttm_zz800PP)
factors.append(OCFP_zz800PP)
factors.append(OCFPttm_zz800PP)
factors.append(SalesP_zz800PP)
factors.append(SalesPttm_zz800PP)
factors.append(Turnover_zz800PP)
factors.append(FreeTurnover_zz800PP)
factors.append(DividendYield_zz800PP)

# # # zBP = BP.Z(False, zz800PP)
# # # zBP_SN = BP.Z(True, zz800PP)
# #
# # # Calculate Scores and Save
# BP_a50PP.CalcScoresAndSave(CacheDts, a50PP)
# for f in factors:
#     f.CalcScoresAndSave(CacheDts, a50PP)

# zBP.CalcScoresAndSave(CacheDts, zz800PP)
# zBP_SN.CalcScoresAndSave(CacheDts, zz800PP)

#SaveWindIndicatorsCache()

print GlobalConstant.REPORT_DIR

# tileAnalysis = TileAnalysis(SatDts, zz800PP, 5)
# tileAnalysis.Run(BP_zz800PP)
#tileAnalysis = TileAnalysisReport(SatDts, zz800PP, 5)
#tileAnalysis.Run(BP_zz800PP, True)
#tileAnalysis.Report(factor=BP_zz800PP, reportFileName=GlobalConstant.REPORT_DIR+'BP_zz800_1.pdf', bmDemean=True)
#tileAnalysis.Report(factor=BP_zz800PP,  reportFileName=GlobalConstant.REPORT_DIR+'BP_zz800_0.pdf', bmDemean=False)

for f in factors:
    ta = TileAnalysis(SatDts, f, zz800PP, 5, True)
    ta.GenReport(GlobalConstant.REPORT_DIR+str(f.Name) + '_zz800_1.pdf')


# taBP1 = TileAnalysis(SatDts, BP_zz800PP, zz800PP, 5, True)
# taBP1.GenReport(GlobalConstant.REPORT_DIR+'BP_zz800_1.pdf')
#
# taEP1 = TileAnalysis(SatDts, EP_zz800PP, zz800PP, 5, True)
# taEP1.GenReport(GlobalConstant.REPORT_DIR+'EP_zz800_1.pdf')
#
# taEPttm1 = TileAnalysis(SatDts, EPttm_zz800PP, zz800PP, 5, True)
# taEPttm1.GenReport(GlobalConstant.REPORT_DIR+'EPttm_zz800_1.pdf')
#
# taCFP1 = TileAnalysis(SatDts, CFP_zz800PP, zz800PP, 5, True)
# taCFP1.GenReport(GlobalConstant.REPORT_DIR+'CFP_zz800_1.pdf')
#
# taCFPttm1 = TileAnalysis(SatDts, CFPttm_zz800PP, zz800PP, 5, True)
# taCFPttm1.GenReport(GlobalConstant.REPORT_DIR+'CFPttm_zz800_1.pdf')
#
# taOCFP1 = TileAnalysis(SatDts, OCFP_zz800PP, zz800PP, 5, True)
# taOCFP1.GenReport(GlobalConstant.REPORT_DIR+'OCFP_zz800_1.pdf')
#
# taOCFPttm1 = TileAnalysis(SatDts, OCFPttm_zz800PP, zz800PP, 5, True)
# taOCFPttm1.GenReport(GlobalConstant.REPORT_DIR+'OCFPttm_zz800_1.pdf')
#
# taSalesP1 = TileAnalysis(SatDts, OCFP_zz800PP, zz800PP, 5, True)
# taSalesP1.GenReport(GlobalConstant.REPORT_DIR+'OCFP_zz800_1.pdf')
#
# taSalesPttm1 = TileAnalysis(SatDts, SalesPttm_zz800PP, zz800PP, 5, True)
# taSalesPttm1.GenReport(GlobalConstant.REPORT_DIR+'SalesPttm_zz800_1.pdf')
#
# taTO1 = TileAnalysis(SatDts, Turnover_zz800PP, zz800PP, 5, True)
# taTO1.GenReport(GlobalConstant.REPORT_DIR+'Turnover_zz800_1.pdf')
#
# taFreeTO1 = TileAnalysis(SatDts, FreeTurnover_zz800PP, zz800PP, 5, True)
# taFreeTO1.GenReport(GlobalConstant.REPORT_DIR+'FreeTurnover_zz800_1.pdf')
#
# taDivYld1 = TileAnalysis(SatDts, DividendYield_zz800PP, zz800PP, 5, True)
# taDivYld1.GenReport(GlobalConstant.REPORT_DIR+'DividendYield_zz800_1.pdf')


#tileAnalysis.Report(factor=CFP_zz800PP,  reportFileName=GlobalConstant.REPORT_DIR+'BP_zz800_0.pdf', bmDemean=False)