%% header
% store all constant variables that can be accessed globally
% date: 7/17/2015

%%

classdef GlobalConstant       
    properties (Constant)
        % locations
        BASE_DIR = 'd:\ChinaA\';
        CODE_DIR = 'd:\ChinaA\source\';
        DATA_DIR = 'd:\ChinaA\data\';
        
        % test start and end date
        TestStartDate = '20081231';
        TestEndDate = '20141231';
        
        % database connection
        DBCONN_WIND = database('WindDB','','','Vendor','Microsoft SQL Server','Server','localhost','AuthType','Windows','PortNumber',1433);
        
        % exchange trading dates
        TradingDates = QDate.GetAllTradingDays();
        
        % holding structure
        Holding = {'StockID', 'Weight', 'Shares', 'MarketValue'};
    end
end
