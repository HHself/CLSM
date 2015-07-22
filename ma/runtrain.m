function runtrain()

wordvecpath = '/home/huhao/dssm/output/doc_vec.txt';
flagpath = '/home/huhao/dssm/output/doc_flag.txt';
wordvecpath = 'doc_vec.txt';
flagpath = 'doc_flag.txt';
cd = 32;
od = 32;
fw = 3;
gama = 10;
eta = 0.01;

wordvec = load(wordvecpath);
flag = load(flagpath);

[m, n] = size(flag);
[~, nn] = size(wordvec);

wc=rand(cd, fw*nn) * 10^-2;
ws=rand(od, cd) * 10^-2;


num = 0;
lossd = 0;
disp('success...')
while 1
    lo = 0;
    ind = 1;
    num = num+1;
    disp(num);
    for i=1:m
        [wc, ws, loss] = dssmtrain(wordvec(ind:flag(i,n)+ind-1,:), flag(i,:), wc, ws, n-2, gama, eta);
        ind = ind+ flag(i,n) ;
        lo = lo + loss;
    end
    lossing = lo - lossd
    lossd = lo ;
    if lossing > 0 
        eta = eta *0.1;
    end
    if abs(lossing) < 0.2
        break
    end
end
disp('success...')
save wc.txt wc -ascii
save ws.txt ws -ascii

