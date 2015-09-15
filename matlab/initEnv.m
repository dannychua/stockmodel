%% header
% initialize the environment variables
% date: 7/3/2015

%%
clear all;
clc;

%%
% test variables
stkid = '600048.SH';  %'600090.SH'
dataStartDate = '20081231';
dataEndDate = '20150110';
%sqlString = ['select TRADE_DT, S_DQ_ADJCLOSE from WindDB.dbo.ASHAREEODPRICES  where S_INFO_WINDCODE = ''', stkid, ''' order by trade_dt'];

% set working directory
addpath('D:/ChinaA/source' ,'D:/ChinaA/source/Common', 'D:/ChinaA/source/FactorLib')
% global BASE_DIR;
% global CODE_DIR;
% global DATA_DIR;
% BASE_DIR = 'd:\ChinaA\';
% CODE_DIR = fullfile(BASE_DIR, 'source');
% DATA_DIR = fullfile(BASE_DIR, 'data');

% it is time consuming to construct a Stock instance
% the variable below is used to store all stocks by their WindID
% so that one stock is initialized only once
global STOCKMASTERMAP;
STOCKMASTERMAP = containers.Map();

% 
% % database connection
% global DBCONN_WIND;
% DBCONN_WIND = database('WindDB','','','Vendor','Microsoft SQL Server','Server','localhost','AuthType','Windows','PortNumber',1433);
