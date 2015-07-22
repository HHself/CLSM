function  [wc, ws, lossfunc] = dssmtrain(wordvector, flag, wc, ws, batch, gama, eta)

%use mini-batch stochastic gradient decent(SGD) to train wc, ws which are
%  parameter for dssm

%wordvector is the train data whose first raw is the source vector,second 
%  is positive vector and the rest of vector is the negative vector
%flag are flags and 1*(batch+2) vector shows that positive sample or negative sample
%cd, od, fw is the same with dssm.m
%batch is the number of mini-batch, gama is the para. of loss function, 
% eta is the learning rate

[~, n] = size(wordvector);
[mm, nn] = size(ws);
[mmm, nnn] = size(wc);
 
% flag(1)+1
% flag(2)
% size(wordvector(flag(1)+1:flag(2),1:n))
%flg = flag(1)
%[m , n]=size(wordvector)
%wv = wordvector(1:flag(1),1:n)
[ys, vs, ts, ls, ~]= dssm(wordvector(1:flag(1),:), wc, ws);
% wordvector(flag(1)+1:flag(2),1:n)
[yp, vp, tp, lp, ~]= dssm(wordvector(flag(1)+1:flag(2),:), wc, ws); 
sprel = cosrel(ys, yp);
nsum = 0;
%cal alpha j
for i=2:batch+1
    [yn, ~, ~, ~, ~]= dssm(wordvector(flag(i)+1:flag(i+1),:), wc, ws);
    snrel = cosrel(ys, yn);  
    nsum = nsum + exp(-gama *(sprel-snrel));
end

%nsum
%cal gradient of ws and wc
gradientws = zeros(mm, nn);
gradientwc = zeros(mmm, nnn);
for j=2:batch+1
    [yn, vn, tn, ln, ~]= dssm(wordvector(flag(j)+1:flag(j+1),:), wc, ws);
    snrel = cosrel(ys, yn);
    alphaj = (-gama * exp(-gama * (sprel-snrel))) / (1 + nsum);
    gradientws = gradientws + alphaj * (reldiffws(ys ,yp, vs ,vp) - reldiffws(ys, yn, vs, vn));
    
    sigmavsps = sigmavqd(vs, ws, ys, yp);
    sigmavspp = sigmavqd(vp, ws, yp, ys);
    sigmavsns = sigmavqd(vs, ws ,ys, yn);
    sigmavsnn = sigmavqd(vn, ws, yn, ys);
    for k=1:mmm
        gra =alphaj * ((sigmavsps(k) * ls(ts(k),:) + sigmavspp(k) * lp(tp(k),:)) - (sigmavsns(k) * ls(ts(k),:) + sigmavsnn(k) * ln(tn(k),:)));
        gradientwc(k, :) =  gradientwc(k, :) + gra;
    end
end
%update ws and wc
%gradientws
%gradientwc
%wss = ws(1,1:3)
%wcc = wc(1,1:3)
%gws = gradientws(1,1:3)
%gwc = gradientwc(1,1:3)
%disp('***********************')
ws = ws - eta * gradientws;
wc = wc - eta * gradientwc;

%get loss
delta = 0;
[ys, ~, ~, ~, ~]= dssm(wordvector(1:flag(1),:), wc, ws);
[yp, ~, ~, ~, ~]= dssm(wordvector(flag(1)+1:flag(2),:), wc, ws); 
sprel = cosrel(ys, yp);

for j=2:batch+1
   [yn, ~, ~, ~, ~]= dssm(wordvector(flag(j)+1:flag(j+1),1:n), wc, ws);
    snrel = cosrel(ys, yn);
    delta = delta + exp(-10 * (sprel - snrel));
end
lossfunc = log(1 + delta);
