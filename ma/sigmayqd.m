function res = sigmayqd(yq, yd)

%cal sigma yq, ys for (Q,D)
a = yq * yd';
b = 1 / norm(yq);
c = 1 / norm(yd);
res = (1 - yq) .* (1 - yq) .* ( b * c * yd - a * c * b^3 * yq);
