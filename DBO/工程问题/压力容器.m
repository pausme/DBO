%Pressure vessel design
function [objF, conV]=problem_1(P)

g = [];

% g denotes the constraints
% f denotes the objective function
%R,L,Ts,Th----1,2,3,4

g(:, 1) = - P(:, 3) + 0.0193 * P(:, 1);
g(:, 2) = - P(:, 4) + 0.00954 * P(:, 1);
g(:, 3) = - pi * P(:, 1).^2 .* P(:, 2) - (4/3) * pi * P(:, 1).^3 + 750*1728;
g(:, 4) = P(:, 2) - 240;

f = 0.6224 * P(:, 3) .* P(:, 1) .* P(:, 2) + 1.7781 * P(:, 4) .* P(:, 1).^2 + 3.1611 * P(:, 3).^2 .* P(:, 2) + 19.84 * P(:, 3).^2 .* P(:, 1);

% Obtain the fitness
objF= f;
term = max(0, g);
conV = sum(term, 2);