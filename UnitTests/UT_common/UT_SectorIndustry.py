from common.SectorIndustry import *

def UnitTests():
    # 1st time access,if no data file exists, run database query
    numDts = len(SectorIndustry.WINDIndustry);
    print("1st time Num of Dates: " + numDts)
    # 2nd time access, load it from the file
    numDts = len(SectorIndustry.WINDIndustry);
    print("2nd time Num of Dates: " + numDts)

if __name__ == '__main__':
    UnitTests()
    pass