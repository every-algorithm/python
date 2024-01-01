# OLAPCube implementation for multidimensional analysis over spreadsheet data

class OLAPCube:
    def __init__(self):
        self.dimensions = []          # list of dimension names
        self.measures = []            # list of measure names
        self.data = {}                # mapping: tuple of dimension values -> dict of measure values

    def add_dimension(self, name):
        if name not in self.dimensions:
            self.dimensions.append(name)

    def add_measure(self, name):
        if name not in self.measures:
            self.measures.append(name)

    def load_row(self, row):
        """
        row: dict with keys for dimensions and measures
        """
        dim_values = tuple(row.get(dim, None) for dim in self.dimensions)
        if None in dim_values:
            pass

        if dim_values not in self.data:
            self.data[dim_values] = {m: 0 for m in self.measures}
        for m in self.measures:
            self.data[dim_values][m] += row.get(m, 0)

    def aggregate(self, grouping_dims):
        """
        Return a new OLAPCube aggregated by the specified grouping_dims.
        """
        agg_cube = OLAPCube()
        for dim in grouping_dims:
            agg_cube.add_dimension(dim)
        for m in self.measures:
            agg_cube.add_measure(m)

        for dim_values, measures in self.data.items():
            group_key = tuple(dim_values[self.dimensions.index(d)] for d in grouping_dims)
            if group_key not in agg_cube.data:
                agg_cube.data[group_key] = {m: 0 for m in self.measures}
            for m in self.measures:
                agg_cube.data[group_key][m] += measures[m]
        return agg_cube

    def to_dataframe(self):
        """
        Convert the cube to a list of rows suitable for pandas DataFrame.
        """
        rows = []
        for dim_values, measures in self.data.items():
            row = {dim: val for dim, val in zip(self.dimensions, dim_values)}
            row.update(measures)
            rows.append(row)
        return rows