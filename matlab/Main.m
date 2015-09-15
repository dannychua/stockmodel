% Test cases
%     stkid = '600230.SH';  
%     date = '20141008';


%%
% addpath('D:/ChinaA/source' ,'D:/ChinaA/source/Common', 'D:/ChinaA/source/FactorLib')
% initEnv
% a50PP = PortfolioProviders.GetA50();
% 
% BP = Factor('BP','Book/Price',@BPCalc);

stkid = '600048.SH';  
date = '20090404';
date = datenum(date, 'yyyymmdd');
GetScore(BP, stkid, date, true)

%stk = Stock.ByWindID(stkid);

StockMasterCache = 'd:\ChinaA\data\StockMaster';
load(StockMasterCache); % load STOCKMASTERMAP from cache
%save(StockMasterCache,'STOCKMASTERMAP');


%%%%%%%%% unit tests
% ret1 = TotalReturnInRange(stk, '20140101','20141231')
% ret1 = TotalReturnInRange(stk, '20000101','20141231')
% ret1 = TotalReturnInRange(stk, '20140101','20140105')
% price = PriceOnDate(stk, '20140101')
% mktCap = FloatMarketCap(stk, '20150112')

% a50Pf= GetPortfolioOn(a50PP, '20141231');
% ret2 = TotalReturnInRange(a50Pf, '20140101','20141231')

tileAnalysis = TileAnalysis(WkDts, zz800PP, 3);
%[BPQ1Rets, BPQ5Rets, BPSpreads] = Run(tileAnalysis, BP, true);
[BPQ1Rets, BPQ5Rets, BPSpreads] = Run(tileAnalysis, zBP, true);
% plot(BPQ1Rets, 'cr', 'Q1');
% plot(BPQ5Rets, 'cr', 'Q5');
% plot(BPSpreads, 'cr', 'Q1/Q5');

