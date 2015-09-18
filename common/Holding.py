# %% header
# % handle a holding and the related logic
# % date: 7/3/2015

# %%
# % it is a handle class
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% not needed


class Holding():
    def __init__(self, stock, weight, shares=None, marketValue=None):
        self.StockID = stock              # the stockID held
        self.Weight = weight              # number of shares held, could be negative or null
        self.Shares = shares
        self.MarketValue = marketValue    #the market value of the holding, could be negative or null

