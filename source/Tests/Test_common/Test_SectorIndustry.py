from source.common.Stock import *

def test_SectorIndustry():
    sectorInd = SectorIndustry();
    # 1st time access,if no data file exists, run database query
    numDts = len(sectorInd.WINDIndustry);
    print("1st time Num of Dates: " + str(numDts))
    # 2nd time access, load it from the file
    numDts = len(sectorInd.WINDIndustry);
    print("2nd time Num of Dates: " + str(numDts))
    print type(sectorInd.WINDIndustry)

    windID = '600048.SH'
    date = Str2Date('20140101')  # New Year Holiday
    #a = SectorIndustry.loadWINDIndustry()

    ts = sectorInd.WINDIndustry[windID]
    indCode = ts.ValueAsOf(date)
    print([indCode, indCode[0:4]])

test_SectorIndustry()
