function [J, grad] = linearRegCostFunction(X, y, theta, lambda)
%LINEARREGCOSTFUNCTION Compute cost and gradient for regularized linear 
%regression with multiple variables
%   [J, grad] = LINEARREGCOSTFUNCTION(X, y, theta, lambda) computes the 
%   cost of using theta as the parameter for linear regression to fit the 
%   data points in X and y. Returns the cost in J and the gradient in grad

% Initialize some useful values
m = length(y); % number of training examples

% You need to return the following variables correctly 
J = 0;
grad = zeros(size(theta));


% ====================== YOUR CODE HERE ======================
% Instructions: Compute the cost and gradient of regularized linear 
%               regression for a particular choice of theta.
%
%               You should set J to the cost and grad to the gradient.
%
for i = 1:m
    h = theta' * X(i,:)';
    J = J + (h-y(i))^2;
    
end
J = (1/(2*m)) * J;
theta_sum = sum(theta .^ 2) - theta(1)^2;
J = J + (lambda/ (2*m)) * theta_sum;


for j = 1:size(theta)
    for i = 1:m
        h = theta' * X(i,:)';
        grad(j) = grad(j) + (h - y(i)) * X(i,j);
    end
    grad(j) = (1/m) * grad(j);
    if j ~= 1
        grad(j) = grad(j) + (lambda / m) * theta(j);
    end
end









% =========================================================================

grad = grad(:);

end
