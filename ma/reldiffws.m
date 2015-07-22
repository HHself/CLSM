function [res] = reldiffws(yq, yd, vq, vd)

% rel(q,d) diff ws
%yq, yd are the output of dssm and vd, vq are the output of cnn in dssm

%sigmaq = sigmayqd(yq, yd);
%sigmad = sigmayqd(yd, yq);

a = yq * yd';
b = 1.0 / norm(yq);
c = 1.0 / norm(yd);

sigmaq = (1 - yq) .* (1 + yq) .* (b * c * yd - a * c * b^3 * yq);
sigmad = (1 - yd) .* (1 + yd) .* (b * c * yq - a * b * c^3 * yd);

res = vq' * sigmaq + vd' * sigmad;
res = res';
