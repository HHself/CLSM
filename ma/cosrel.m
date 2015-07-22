function r= cosrel(a, b)

%calculate the cosine simi. between vector a and vetor b
r = (a * b') / (norm(a) * norm(b));