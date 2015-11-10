__author__ = 'xiaofeng'

def CovMat_PC(dailyReturns, pctExplained):
    pass

# function covmat = PCA(dailyRets, pctExplained)
#
# T = size(dailyRets, 1);  % number of periods
# N = size(dailyRets, 2);  % number of stocks
#
# % demean daily returns
# colMean = mean(dailyRets,1);
# demeanRets = dailyRets - ones(T,1)*colMean;
#
# % generate a N by N covmat
# sampleCovmat = demeanRets' * demeanRets / (T-1);
# % when N > T, use AsymptoticPCA and a T by T covmat is generated
# % sampleCovmat = demeanRets * demeanRets' / (N-1);
#
# % eigen-value/vector decomposition
# [E,L,explained] = pcacov(sampleCovmat);
#
# % the number of principle components which explains more than
# % "pctExplained" of the total variance
# NumPC = 0;
# R2 = pctExplained * sum(explained);
# tmp = 0;
# for i = 1:N
#     tmp = tmp + explained(i);
#     if(tmp > R2)
#         NumPC = i;
#         break;
#     end
# end
#
# E = E(:, 1:NumPC);
# L = L(1: NumPC);
#
# % portfolio returns T by NumPC
# B = demeanRets * E;
#
# % residual returns
# resiRets = demeanRets - B * E';
#
# scalar = 252; % scalar to annualize covmat
# specVar = scalar * var(resiRets,0,1);
# c = scalar * E* (B' * B)*E' / T + diag(specVar);
#
# % make sure it is symmetric
# covmat = (c+c')*0.5;