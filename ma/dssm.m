function [y, v, t, lt, keyind] = dssm(wordvector, wc, ws)

%DSSM infer
%wordvector is a matrix and each row representation of a word vector
%cd is the operation dimention of cnn and od is the dimention of output featrue
%fw is the fix windows
%wc is the parameter of cnn, dim is cd * dim. of concate words vector
%ws is the parameter of semantic layer, dim. is od * cd
%t is the local feature that win in the max+
%v is the output of cnn and y is the output of dssm

%add the vector of # in wordvector 
[~, n] = size(wordvector);
z = zeros(1,n);
wordvector = [z;wordvector];
wordvector = [wordvector;z];

%cnn 
[v, t, lt, keyind] = cnn(wordvector, wc);
%cnn to output layer
y = tanh(v * ws');
