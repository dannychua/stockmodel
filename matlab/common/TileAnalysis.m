%% header
% the tile analysis is to put all stocks into equally sized groups and the number of groups is defined by Tile
% and then construct tile portfolios for each tile either equally or cap-weighted.
% analyze the time series returns of each tile portfolio

% Date: 8/2/2015

%%

classdef TileAnalysis < handle
    
    properties
        NumTiles       % the number of tiles
        Dates          % the testing dates 
        UnivPP         % universe portfolio provier
    end
    
    methods
        function obj = TileAnalysis(dates, univPP, numTiles)
            if ischar(dates)
                obj.Dates = datenum(dates,'yyyymmdd');
            else
                obj.Dates = dates;
            end
            
            obj.UnivPP = univPP;
            
            if (nargin>2) 
                obj.NumTiles = numTiles;
            else
                obj.NumTiles = 5;
            end
        end
        
        
        function [topTileRets, botTileRets, spreads] = Run(obj, factor, bmDemean)
            periods = length(obj.Dates)-1;
            topTileRets = ReturnSeries();
            botTileRets = ReturnSeries();
            spreads = ReturnSeries();
            
            BMDemean = false;
            if(nargin>2 && bmDemean==true)
                BMDemean = true;
            end
            
            for i = 1:periods
                dt = obj.Dates(i);
                nextdt = obj.Dates(i+1);
                portfolio = GetPortfolioAsofFixed(obj.UnivPP, dt, 0);
                stockIDs = GetStockIDs(portfolio);
                %scores = arrayfun(@(stkid) GetScore(BP, stkid,dt),stockIDs);  doesn't work due to string array treated as char matrix
                
                % calculate factor scores and sort them
                totNumStks = length(stockIDs);
                scores = zeros(totNumStks,1);
                for j=1:totNumStks
                    scores(j) = GetScore(factor, stockIDs(j,:),dt, 1);
                end
                
                % nan scores are on the top
                [scoresSortedDown, idx] = sort(scores,'descend');
                numNaNs = sum(isnan(scores));
                if(numNaNs/totNumStks > 0.5)
                    error('Half of stocks have NaN scores')
                end
                
                numStkInTile = floor((totNumStks-numNaNs) / obj.NumTiles);
                
                topTileStkRets = zeros(numStkInTile,1);
                botTileStkRets = zeros(numStkInTile,1);
                for j=1:numStkInTile
                    topTileStkRets(j) = TotalReturnInRange_Bk(Stock.ByWindID(stockIDs(idx(j+numNaNs),:)), dt, nextdt);
                    botTileStkRets(j) = TotalReturnInRange_Bk(Stock.ByWindID(stockIDs(idx(totNumStks-j+1),:)), dt, nextdt);
                end
                
                % equal weighted for now, later need to check whether it is
                % cap weighted or equal weighted
                topRet = nanmean(topTileStkRets);
                botRet = nanmean(botTileStkRets);
                
                if(BMDemean)
                    bmRet = TotalReturnInRange_Bk(obj.UnivPP, dt, nextdt);
                    topRet = topRet - bmRet;
                    botRet = botRet - bmRet;
                end
                
                Add(topTileRets, nextdt, topRet);
                Add(botTileRets, nextdt, botRet);
                Add(spreads, nextdt, topRet - botRet);
            end
            
            disp(['Top AnnMean, ', num2str(topTileRets.AnnMean)]);
            disp(['Top AnnStd,  ', num2str(topTileRets.AnnStd)]);
            disp(['Top SR,      ', num2str(topTileRets.SR)]);
            
            disp(['Bot AnnMean, ', num2str(botTileRets.AnnMean)]);
            disp(['Bot AnnStd,  ', num2str(botTileRets.AnnStd)]);
            disp(['Bot SR,      ', num2str(botTileRets.SR)]);
            
            disp(['Spread AnnMean, ', num2str(spreads.AnnMean)]);
            disp(['Spread AnnStd,  ', num2str(spreads.AnnStd)]);
            disp(['Spread SR,      ', num2str(spreads.SR)]);
            
        end
              
    end
end