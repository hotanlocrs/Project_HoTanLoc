import numpy as np
import faiss
def faiss_t(embed_vecs, vec, labels):
    xb = np.array(embed_vecs)
    xq = np.array(vec)
    d = len(vec[0])
    index = faiss.IndexFlatL2(d)  # build the index
    index.add(xb)  # add vectors to the index
    k = 5
    D, I = index.search(xq, k)  # actual sea
    return labels[I[0][0]]
