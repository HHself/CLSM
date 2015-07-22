function wordvec = getwordvecmat(wordvecpath, wvm, wvn)

% get flag for training

wordvec = zeros(wvm, wvn);
fidin = fopen(wordvecpath);
n = 0;
while ~feof(fidin)           
   n = n + 1;
   tline = fgetl(fidin);     
   str=tline;       
   sline=sscanf(str,'%f',fn);
   flag(n, 1:fn) = sline';
end
fclose(fidin);