class PortfolioProviders():
    """Generates pre-defined portfolio providers.

        since 4/1/2009, the table AIndexHS300FreeWeight has constituents
        and their weights on a daily basis
        before that, the table AIndexMembers has constituents' in-and-out
        dates, and the index can still be constructed using market cap
        
        To validate: 
        1. the boundary of in-and-out dates, i.e., whether the "out" date
        is the first day of being out or the last date of being in.
        2. is it constructed by total market cap or floating market cap?
    """


    @staticmethod
    def getA50():
    	return 'A50 object'


    @staticmethod
    def getZhongZheng500():
    	pass


    @staticmethod
    def getZhongZheng800():
    	pass


    @staticmethod
    def getClosingPx(idxWindID):
    	pass


    @staticmethod
    def fetchInBatches(conn, rs, batchCount, maxrows):
    	pass





print PortfolioProviders.getA50()