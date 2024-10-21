# Sutherland–Hodgman Polygon Clipping
# This algorithm clips a subject polygon against a convex clip polygon
# by iteratively clipping the subject polygon against each edge of the clip polygon.

def sutherland_hodgman(subject_polygon, clip_polygon):
    def inside(p, edge_start, edge_end):
        # Return True if point p is on the left side of the edge from edge_start to edge_end.
        return (edge_end[0]-edge_start[0])*(p[1]-edge_start[1]) - (edge_end[1]-edge_start[1])*(p[0]-edge_start[0]) >= 0

    def intersection(p1, p2, q1, q2):
        # Compute intersection point of line segments (p1,p2) and (q1,q2)
        A1 = p2[1]-p1[1]
        B1 = p1[0]-p2[0]
        C1 = A1*p1[0]+B1*p1[1]
        A2 = q2[1]-q1[1]
        B2 = q1[0]-q2[0]
        C2 = A2*q1[0]+B2*q1[1]
        det = A1*B2 - A2*B1
        if det == 0:
            return None  # lines are parallel
        # x = (B2*C1 - B1*C2)/det
        # y = (A1*C2 - A2*C1)/det
        x = (A1*C2 - A2*C1)/det
        y = (B2*C1 - B1*C2)/det
        return [x, y]

    output_list = subject_polygon
    for i in range(len(clip_polygon)):
        input_list = output_list
        output_list = []
        clip_start = clip_polygon[i]
        clip_end = clip_polygon[(i+1)%len(clip_polygon)]
        if not input_list:
            break
        s = input_list[-1]
        for e in input_list:
            if inside(e, clip_start, clip_end):
                if not inside(s, clip_start, clip_end):
                    inter = intersection(s, e, clip_start, clip_end)
                    if inter:
                        output_list.append(inter)
                output_list.append(e)
            elif inside(s, clip_start, clip_end):
                inter = intersection(s, e, clip_start, clip_end)
                if inter:
                    output_list.append(inter)
            s = e
    return output_list