function [X_poly] = polyFeatures(X, p)
%POLYFEATURES Maps X (1D vector) into the p-th power
%   [X_poly] = POLYFEATURES(X, p) takes a data matrix X (size m x 1) and
%   maps each example into its polynomial features where
%   X_poly(i, :) = [X(i) X(i).^2 X(i).^3 ...  X(i).^p];
%


% You need to return the following variables correctly.
rows_orig = size(X,1);
cols_orig = size(X,2);
X_poly = zeros(rows_orig, cols_orig * p);
X_poly(:, 1:cols_orig) = X;
% ====================== YOUR CODE HERE ======================
% Instructions: Given a vector X, return a matrix X_poly where the p-th 
%               column of X contains the values of X to the p-th power.
%
%

for i = 2:p
    for j = 1:cols_orig
        X_poly(:, cols_orig * (i-1) + j) = X(:, j) .^ i;
    end
end






% =========================================================================

end
