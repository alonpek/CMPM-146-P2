def next_point(current_box, neighbor_box, detail_points):
    point_cur = detail_points[current_box]

    print('current box:', current_box)
    print('neighbor box:', neighbor_box)

    # min of max and max of min idea to calculate overlapping line segment
    # inspired by: http://pythonshort.blogspot.com/2015/03/intersection-of-two-line-segments-in.html
    right = min(max(current_box[2], current_box[3]), max(neighbor_box[2], neighbor_box[3]))
    left = max(min(current_box[2], current_box[3]), min(neighbor_box[2], neighbor_box[3]))
    top = max(min(current_box[0], current_box[1]), min(neighbor_box[0], neighbor_box[1]))
    bottom = min(max(current_box[0], current_box[1]), max(neighbor_box[0], neighbor_box[1]))

    edge_segment = ((left, bottom), (right, top))
    print(edge_segment)
    print(point_cur)

    point_new = [0, 0]

    # segment is vertical
    if edge_segment[0][0] == edge_segment[1][0]:
        point_new[0] = edge_segment[0][0]

        edge_max = max(edge_segment[0][1], edge_segment[1][1])
        edge_min = min(edge_segment[0][1], edge_segment[1][1])
        # assign y axis
        if point_cur[0] > edge_max:
            point_new[1] = edge_max
        elif point_cur[0] < edge_min:
            point_new[1] = edge_min
        else:
            point_new[1] = point_cur[0]

    # else segment is horizontal
    else:
        point_new[1] = edge_segment[0][1]

        edge_max = max(edge_segment[0][0], edge_segment[1][0])
        edge_min = min(edge_segment[0][0], edge_segment[1][0])
        # assign y axis
        if point_cur[1] > edge_max:
            point_new[0] = edge_max
        elif point_cur[1] < edge_min:
            point_new[0] = edge_min
        else:
            point_new[0] = point_cur[1]

    print(point_new)
    point_new = (point_new[1], point_new[0])
    detail_points[neighbor_box] = point_new

    return point_new
