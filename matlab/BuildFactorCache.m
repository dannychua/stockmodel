%% header
% build factor score cache for all factors
% Date: 7/3/2015

%%
addpath('D:/ChinaA/source' ,'D:/ChinaA/source/Common', 'D:/ChinaA/source/FactorLib')
%initEnv

A50PPCache = 'd:\ChinaA\data\Universes\A50PP';
%a50PP = PortfolioProviders.GetA50();
%save(A50PPCache, 'a50PP');
%load(A50PPCache);  % load a50PP from cache

zz800PPCache = 'd:\ChinaA\data\Universes\zz800PP';
%zz800PP = PortfolioProviders.GetZhongZheng800();
%save(zz800PPCache, 'zz800PP');
load(zz800PPCache);  % load pp from cache
%pf = GetPortfolioAsofFixed(zz800PP, '20141231');
% 

WkDts = QDate.WeekEndsBtw('20090401', '20141231');
MonDts = QDate.MonthEndsBtw('20090401', '20141231');
CacheDts = QDate.UnionDistinct(WkDts,MonDts);

BP = Factor('BP','Book/Price',@BPCalc);
zBP=Z(BP, false, zz800PP);
zBP_SN=Z(BP, true, zz800PP);

% a50PP 2009-04-01 ~ 2014-12-31
%CalcScoresAndSave(BP,a50PP.AvailableDates,a50PP); % tests
CalcScoresAndSave(BP,CacheDts,zz800PP); % tests
CalcScoresAndSave(zBP,CacheDts,zz800PP); % tests
CalcScoresAndSave(zBP_SN,CacheDts,zz800PP); % tests

