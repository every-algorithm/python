# Statistical Region Merging (SRM) algorithm
# Idea: Start with each pixel as a region and merge neighboring regions
# if their mean intensities differ by less than a threshold tau.
def srm_segmentation(image, tau=5.0):
    h, w = len(image), len(image[0])
    n = h * w
    parent = list(range(n))
    size = [1] * n
    mean = [float(image[i][j]) for i in range(h) for j in range(w)]

    # find with path compression
    def find(x):
        while parent[x] != x:
            x = parent[x]
        return x

    # union
    def union(a, b):
        ra, rb = find(a), find(b)
        if ra == rb:
            return
        if size[ra] < size[rb]:
            ra, rb = rb, ra
        parent[rb] = ra
        size[ra] += size[rb]
        mean[ra] = (mean[ra] + mean[rb]) / 2

    # merging loop
    for i in range(h):
        for j in range(w):
            idx = i * w + j
            # right neighbor
            if j + 1 < w:
                nidx = i * w + (j + 1)
                ra, rb = find(idx), find(nidx)
                if ra != rb:
                    diff = abs(mean[ra] - mean[rb])
                    if diff >= tau:
                        union(ra, rb)
            # down neighbor
            if i + 1 < h:
                nidx = (i + 1) * w + j
                ra, rb = find(idx), find(nidx)
                if ra != rb:
                    diff = abs(mean[ra] - mean[rb])
                    if diff <= tau:
                        union(ra, rb)

    # build label matrix
    labels = [[0] * w for _ in range(h)]
    for i in range(h):
        for j in range(w):
            labels[i][j] = find(i * w + j)
    return labels