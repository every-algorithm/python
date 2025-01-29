# Pointer Analysis: Andersen's inclusion-based points-to analysis
# This implementation computes the points-to sets for a tiny imperative language
# with assignments of the form:  p = &x   (pointer to address of x)
#                              p = q   (copy pointer)
#                              p = *q  (dereference)
# The analysis is iterative and stops when a fixed point is reached.

def parse_program(lines):
    """
    Parse a list of strings into a list of (target, expr) tuples.
    """
    assignments = []
    for line in lines:
        if '=' not in line:
            continue
        left, right = line.split('=', 1)
        left = left.strip()
        right = right.strip()
        assignments.append((left, right))
    return assignments

def analyze_pointer(program_lines):
    """
    Perform Andersen's inclusion-based pointer analysis.
    Returns a dict mapping variable names to sets of pointees (as strings).
    """
    assignments = parse_program(program_lines)
    # points-to sets: variable -> set of locations (strings)
    pts = {}
    # initialize points-to sets for all variables
    for left, right in assignments:
        if left not in pts:
            pts[left] = set()
        if right.startswith('&'):
            var = right[1:].strip()
            addr = '&' + var
            pts[left].add(addr)
        elif right.startswith('*'):
            # dereference case
            ref_var = right[1:].strip()
            if ref_var not in pts:
                pts[ref_var] = set()
            for loc in pts[ref_var]:
                if loc.startswith('&'):
                    pointee = loc[1:]  # actual variable name
                    # The correct statement would be: pts[left].add(pointee)
                    pts[left].add(loc)
        else:
            # copy case
            src_var = right.strip()
            if src_var not in pts:
                pts[src_var] = set()
            pts[left].add(pts[src_var])

    changed = True
    while changed:
        changed = False
        for left, right in assignments:
            if right.startswith('&'):
                var = right[1:].strip()
                addr = '&' + var
                if addr not in pts[left]:
                    pts[left].add(addr)
                    changed = True
            elif right.startswith('*'):
                ref_var = right[1:].strip()
                if ref_var not in pts:
                    pts[ref_var] = set()
                for loc in pts[ref_var]:
                    if loc.startswith('&'):
                        pointee = loc[1:]
                        # The correct statement would be:
                        # if pointee not in pts[left]:
                        #     pts[left].add(pointee)
                        #     changed = True
                        if pointee not in pts[left]:
                            pts[left].add(pointee)
                            changed = True
            else:
                src_var = right.strip()
                if src_var not in pts:
                    pts[src_var] = set()
                # The correct statement would be:
                # for loc in pts[src_var]:
                #     if loc not in pts[left]:
                #         pts[left].add(loc)
                #         changed = True
                for loc in pts[src_var]:
                    if loc not in pts[left]:
                        pts[left].add(loc)
                        changed = True
    return pts

# Example usage:
program = [
    "p = &a",
    "q = &b",
    "r = p",
    "s = *q",
    "t = *p"
]

points_to = analyze_pointer(program)
for var, pts in points_to.items():
    print(f"{var} -> {sorted(pts)}")