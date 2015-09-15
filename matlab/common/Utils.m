%% header
% a host to many utility functions
% date: 8/19/2015

%%


classdef Utils       
    methods (Static)
        % rawscores is a vector
        function zscores = WinsorizedZ(rawscores, cap, tolerance)
            Cap = 3.5;
            Tolerance = 0.1;
            if(nargin>1)
                Cap = cap;
                if(nargin >2)
                    Tolerance = tolerance;
                end
            end
            
            len = length(rawscores);
            zscores = zeros(len,1);
            
            avg = nanmean(rawscores);
            stdev = nanstd(rawscores);
            
            if(isnan(avg) || isnan(stdev) || isinf(avg) || isinf(stdev))
                zscores = rawscores;
                return;
            end
            
            zscores = (rawscores-avg)/stdev;
            
            t = 100;
            while (t > Cap +Tolerance)
                avg = nanmean(zscores);
                stdev = nanstd(zscores);
                
                tmpZ = (zscores-avg)/stdev;
                
                for i = 1:len
                    if(tmpZ(i) > Cap)
                        zscores(i) = (Cap+zscores(i))*0.5;
                    elseif (tmpZ(i) < -Cap)
                        zscores(i) = (-Cap+zscores(i))*0.5;
                    else
                        zscores(i) = tmpZ(i);
                    end
                end
                
                max1 = abs(nanmax(zscores));
                min1 = abs(nanmin(zscores));                
                if(isnan(max1) || isnan(min1))
                    return;
                end                
                t = max(max1, min1);
            end
            
            avg = nanmean(zscores);
            stdev = nanstd(zscores);
            zscores = (zscores-avg)/stdev;
        end
        
        % winsorize within each group
        % group is a n by 1 vector of integers, and it could be any classfication, such as sectors        
        function zscores = WinsorizedZByGroup(rawscores, groups, cap, tolerance)
            Cap = 3.5;
            Tolerance = 0.1;
            if(nargin>2)
                Cap = cap;
                if(nargin >3)
                    Tolerance = tolerance;
                end
            end
            
            C = unique(groups);
            numGroups = length(C);
            numStks = length(rawscores);
            zscores = zeros(numStks,1);
            MinStk = 3;
            
            for i = 1:numGroups
                idx = groups==C(i);
                subrawscores = rawscores(idx);
                if(length(subrawscores) < MinStk)
                    warning('Not enough members in one of the groups in WinsorizedZByGroup ');
                    zscores(idx) = nan;
                else
                    zscores(idx) = Utils.WinsorizedZ(subrawscores, Cap, Tolerance);
                end
            end
        end
        
        function UnitTests()
            a = normrnd(2,5,100,1);
            b =[a;1000];
            b1 = (b-mean(b))/std(b);
            bz = Utils.WinsorizedZ(b);
            %[b1(101), bz(101)]
            
            len = length(b);
            groups = zeros(len,1);
            for i = 1:len
                groups(i) = floor(i/10);
            end
            groups(len) = 1;
            bz2 = Utils.WinsorizedZByGroup(b, groups);
            [b1(1), bz(1), bz2(1)]
            [b1(101), bz(101), bz2(101)]
        end
        
        
    end
    
end
