from common.SectorIndustry import *

def UnitTests():
    sectorInd = SectorIndustry();
    # 1st time access,if no data file exists, run database query
    numDts = len(sectorInd.WINDIndustry);
    print("1st time Num of Dates: " + str(numDts))
    # 2nd time access, load it from the file
    numDts = len(sectorInd.WINDIndustry);
    print("2nd time Num of Dates: " + str(numDts))

if __name__ == '__main__':
    UnitTests()
    pass