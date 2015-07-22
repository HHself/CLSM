function flag = getflagmat(flagpath, fm, nsum)

% get flag for training

fn = nsum + 2;
flag = zeros(fm, fn);
fidin = fopen(flagpath);
n = 0;
while ~feof(fidin)                              
   n = n + 1;
   tline = fgetl(fidin);     
   str=tline;       
   sline=sscanf(str,'%f',fn);
   flag(n, 1:fn) = sline';
end
fclose(fidin);