classdef TP1 < PROBLEM
% <problem> <A-Practical Problem>
% Constrained benchmark MOP
% Analytical MINLP problem

%------------------------------- Reference --------------------------------
%  1. A multi-objective mixed-discrete particle swarm optimization 
%     with multi-domain diversity preservation
%  2. A Parametric Optimization Approach for Multiobjective 
%     Engineering Problems involving Discrete Decisions 

    methods
        %% Initialization
        function obj = TP1()
            obj.Global.M = 2;
            if isempty(obj.Global.D)
                obj.Global.D = 6;
            end
            %初始化种群
            
            obj.Global.lower    = ones(1,3)*-100;
            obj.Global.lower    = [obj.Global.lower,zeros(1,3)];
            obj.Global.upper    = ones(1,3)*100;
            obj.Global.upper    = [obj.Global.upper,ones(1,3)];
            obj.Global.encoding = 'real';
            
        end
        %% Calculate objective values
        function PopObj = CalObj(obj,X)
%             D  = size(X,2);
%             for i=4:6
%                 X(:,i) = round(X(:,i));
%             end
            PopObj(:,1) = X(:,1).^2 - X(:,2) + X(:,3) + 3*X(:,4) + 2*X(:,5) + X(:,6);
            PopObj(:,2) = 2*X(:,1).^2 + X(:,2) - 3*X(:,3) - 2*X(:,4) + X(:,5) - 2*X(:,6);
        end
        %% Calculate constraint violations
        function PopCon = CalCon(obj,X)
%             PopObj = obj.CalObj(X);
%             for i=4:6
%                 X(:,i) = round(X(:,i));
%             end
            PopCon(:,1) = 3*X(:,1) - X(:,2) + X(:,3) + 2*X(:,4);
            PopCon(:,2) = 4*X(:,1).^2 + 2*X(:,1) + X(:,2) + X(:,3)+ X(:,4) + 7*X(:,5) - 40;
            PopCon(:,3) = -X(:,1) - 2*X(:,2) + 3*X(:,3) + 7*X(:,6);
            PopCon(:,4) = -X(:,1) + 12*X(:,4) - 10;
            PopCon(:,5) = X(:,1) - 2*X(:,4) - 5;
            PopCon(:,6) = -X(:,2) + X(:,5) - 20;
            PopCon(:,7) = X(:,2) - X(:,5) - 40;
            PopCon(:,8) = -X(:,3) + X(:,6) - 17;
            PopCon(:,9) = X(:,3) - X(:,6) - 25;
        end
%         %% Sample reference points on Pareto front
%         function P = PF(obj,N)
%             P(:,1) = (0:1/20:1)';
%             P(:,2) = 1 - P(:,1);
%         end
    end

end