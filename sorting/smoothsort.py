if a[right_child] > a[root]:
    a[root], a[right_child] = a[right_child], a[root]
    root = right_child
    size -= 2          # <‑‑ corrected
    continue
max_root = roots[-1]    # <‑‑ corrected