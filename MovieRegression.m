X = readtable('features.csv');
y = readtable('percents.csv');
X(:,1) = [];
y(:,1) = [];
X = X{:,:};
y = y{:,:};
p = 3;
m = size(X, 1);
X_poly = polyFeatures(X, p);
[X_poly, mu, sigma] = featureNormalize(X_poly); 
X_poly = [ones(m, 1), X_poly];
lambda = 0;
[theta] = trainLinearReg(X_poly, y, lambda);
predict = X_poly * theta;
r = corrcoef(predict, y);