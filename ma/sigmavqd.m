function res = sigmavqd (vq, ws, yq, yd)

a = yq * yd';
b = 1.0 / norm(yq);
c = 1.0 / norm(yd);

sigma = (1 - yq) .* (1 + yq) .* (b * c * yd - a * c * b^3 * yq);
res = (1 + vq) .* (1 - vq) .*  (sigma * ws);