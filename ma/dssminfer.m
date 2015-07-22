function dssminfer()
%function dssminfer(wordvectorpath , flagpath,  fw, wcpath, wspath)
%infer keywords, semantic vec to a sentence with wordwector
%dssminfer('checkdoc.txt', 'checkfla.txt',3,  'wc.txt', 'ws.txt') 
%wordvec = load(wordvectorpath);
%flag = load(flagpath);
%wc = load(wcpath);
%ws = load(wspath);


wordvec = load('checkdoc.txt');
flag = load('checkfla.txt');
fw = 3;
wc = load('wc.txt');
ws = load('ws.txt');

[m, n] = size(flag);
[~, nn] = size(wordvec);
[mmm, ~] = size(ws);
ymat = zeros(m, mmm);
kmat = zeros(m, max(max(flag)));

ind = 1;
for i=1:m
    i
    [y, ~, ~, ~, keyind] = dssm(wordvec(ind:flag(i)+ind-1,:), wc, ws);
    ind = ind+ flag(i) ;
    ymat(i, :) = y;
    %for j=1:flag(i)
    
%    kmat(i, j) = keyind(j);
%    end
end


save ymat.txt ymat -ascii
save kmat.txt kmat -ascii
