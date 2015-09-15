%% header
% handle a holding and the related logic
% date: 7/3/2015

%%
% it is a handle class
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% not needed 
% classdef Holding < handle
%     properties
%         StockID         % the stockID held
%         Weight          % weight in a portfolio, could be negative
%         Shares          % number of shares held, could be negative or null
%         MarketValue     % the market value of the holding, could be negative or null
%     end
%     
%     methods
%         function obj = Holding(n)
%             
%         end
%         
%         function obj = Holding(stock, weight, shares, marketValue)
%             obj.Stock = stock;
%             obj.Weight = weight;
%             if(nargin>2) 
%                 obj.Shares = shares;
%                 obj.MarketValue = marketValue;
%             end
%         end        
%         
%     end
%     
% end
