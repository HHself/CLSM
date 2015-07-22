function ot = jugmax(vec)

% judge espetially large number in vec 
% if max - se max > 2(se max - third max) , exsit

[ma, n] = max(vec);
[mm, nn] = size(vec);
summ = sum(vec);
%svec = sort(vec);
%if ma - svec(end-1) > 2 * (svec(end-1) - svec(end-2))
if ma/summ > 2*(1/nn)
    ot = n;
else
    ot = -1;
end
