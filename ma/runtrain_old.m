function runtrain()

wordvecpath = '/home/huhao/dssm/output/doc_vec.txt'
flagpath = '/home/huhao/dssm/output/doc_flag.txt'
cd = 45
od = 45
fw = 3
gama = 10
eta =1.0


flag = load(wordvecpath);
wordvec = load(flagpath);

[m, n] = size(flag);
[~, nn] = size(wordvec);

wc=ones(cd, fw*nn);
ws=ones(od, cd);


num = 0;
while eta > 0.0001 || num < 20
    ind = 1;
    num = num+1;
    disp(num);
    for i=1:m
        [wc, ws] = dssmtrain(wordvec(ind:flag(i,n)+ind-1,1:nn), flag(i, 1:n), fw, wc, ws, n-2, gama, eta);
        ind = ind+ flag(i,n) ;
    end
    
    eta = eta * 0.5;
    
end


save wc.txt wc -ascii
save ws.txt ws -ascii

