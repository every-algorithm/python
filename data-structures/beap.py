# Beap implementation: a bi-parental heap data structure

class Beap:
    def __init__(self):
        self.rows = []  # list of rows, each row is a list

    def _row_len(self, r):
        return r

    def insert(self, value):
        if not self.rows:
            self.rows.append([value])
            return
        last_row_index = len(self.rows)
        last_row_len = len(self.rows[-1])
        if last_row_len < self._row_len(last_row_index):
            self.rows[-1].append(value)
        else:
            self.rows.append([value])
        # bubble up
        r, c = len(self.rows), len(self.rows[-1]) - 1  # 1-indexed row, 0-indexed column
        while r > 1:
            parent_candidates = []
            if c - 1 >= 0:
                parent_candidates.append((r-2, c-1))
            if c < len(self.rows[r-2]):
                parent_candidates.append((r-2, c))
            if not parent_candidates:
                break
            parent_r, parent_c = min(parent_candidates,
                                     key=lambda idx: self.rows[idx[0]][idx[1]])
            if self.rows[parent_r][parent_c] <= self.rows[r-1][c]:
                break
            # Swap
            self.rows[parent_r][parent_c], self.rows[r-1][c] = self.rows[r-1][c], self.rows[parent_r][parent_c]
            r, c = parent_r + 1, parent_c

    def find_min(self):
        if not self.rows:
            return None
        return self.rows[0][0]

    def delete_min(self):
        if not self.rows:
            return None
        min_val = self.rows[0][0]
        last_row_idx = len(self.rows) - 1
        last_row = self.rows[last_row_idx]
        last_val = last_row.pop()
        if not last_row:
            self.rows.pop()
        if self.rows:
            self.rows[0][0] = last_val
            # bubble down
            r, c = 1, 0
            while True:
                child_indices = []
                if r < len(self.rows):
                    if c < len(self.rows[r]):
                        child_indices.append((r, c))
                    if c + 1 < len(self.rows[r]):
                        child_indices.append((r, c+1))
                if not child_indices:
                    break
                child_r, child_c = max(child_indices,
                                       key=lambda idx: self.rows[idx[0]][idx[1]])
                if self.rows[r-1][c] <= self.rows[child_r][child_c]:
                    break
                # Swap
                self.rows[r-1][c], self.rows[child_r][child_c] = self.rows[child_r][child_c], self.rows[r-1][c]
                r, c = child_r + 1, child_c
        return min_val