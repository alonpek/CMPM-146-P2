# Alon Pekurovsky# Dean Rabinowitzfrom heapq import heappop, heappushimport numpydef find_path (source_point, destination_point, mesh):    """    Searches for a path from source_point to destination_point through the mesh    Args:        source_point: starting point of the pathfinder        destination_point: the ultimate goal the pathfinder must reach        mesh: pathway constraints the path adheres to    Returns:        A path (list of points) from source_point to destination_point if exists        A list of boxes explored by the algorithm    """    # Step 1: See method desc    start_box, dest_box = find_start_dest(source_point, destination_point, mesh)    # Step 2: Implement A*    path = []    forward_parent_box = {}    backward_parent_box = {}    forward_dist = {}    backward_dist = {}    forward_dist[start_box] = 0    backward_dist[dest_box] = 0    queue = [(0, start_box, 'destination'), (0, dest_box, 'source')]    forward_detail_points = {}    backward_detail_points = {}    forward_detail_points[start_box] = source_point    backward_detail_points[dest_box] = destination_point    found = False    while len(queue) != 0:        current_dist, current_box, direction = heappop(queue)        if direction is 'destination':            if current_box in backward_dist:                found = True                break            for neighbor_box in mesh['adj'][current_box]:                current_point = forward_detail_points[current_box]                next_point = get_next_point(current_box, neighbor_box, forward_detail_points)                new_dist = forward_dist[current_box] + get_dist(current_point, next_point)                if neighbor_box not in forward_dist or new_dist < forward_dist[neighbor_box]:                    forward_detail_points[neighbor_box] = next_point                    forward_dist[neighbor_box] = new_dist                    queue_dist = new_dist + get_dist(next_point, destination_point)                    heappush(queue, (queue_dist, neighbor_box, 'destination'))                    forward_parent_box[neighbor_box] = current_box        else:            if current_box in forward_dist:                found = True                break            for neighbor_box in mesh['adj'][current_box]:                current_point = backward_detail_points[current_box]                next_point = get_next_point(current_box, neighbor_box, backward_detail_points)                new_dist = backward_dist[current_box] + get_dist(current_point, next_point)                if neighbor_box not in backward_dist or new_dist < backward_dist[neighbor_box]:                    backward_detail_points[neighbor_box] = next_point                    backward_dist[neighbor_box] = new_dist                    queue_dist = new_dist + get_dist(next_point, source_point)                    heappush(queue, (queue_dist, neighbor_box, 'source'))                    backward_parent_box[neighbor_box] = current_box    all_boxes = {**forward_parent_box, **backward_parent_box}    if found:        overlap_box = current_box        while current_box in forward_parent_box:            p1 = forward_detail_points[current_box]            p2 = forward_detail_points[forward_parent_box[current_box]]            path.append((p1, p2))            current_box = forward_parent_box[current_box]        path = path[::-1]        # APPEND THE MIDDLE EDGE        path.append((forward_detail_points[overlap_box], backward_detail_points[overlap_box]))        while overlap_box in backward_parent_box:            p1 = backward_detail_points[overlap_box]            p2 = backward_detail_points[backward_parent_box[overlap_box]]            path.append((p1, p2))            overlap_box = backward_parent_box[overlap_box]        return path, all_boxes.keys()    if not found:        return None, all_boxes.keys()def find_start_dest(source_point, destination_point, mesh):    """    Step 1: identify which boxes contain source and destination    """    for box in mesh['boxes']:        if box[3] >= source_point[1] >= box[2]:            if box[1] >= source_point[0] >= box[0]:                start_box = box        if box[3] >= destination_point[1] >= box[2]:            if box[1] >= destination_point[0] >= box[0]:                dest_box = box    return start_box, dest_boxdef get_dist(p1, p2):    """    Calculate the Euclidean distance between two tuples.    """    a = numpy.array(p1)    b = numpy.array(p2)    dist = numpy.sqrt(numpy.sum((a-b)**2))    return distdef get_next_point(current_box, neighbor_box, detail_points):    point_cur = detail_points[current_box]    # min of max and max of min idea to calculate overlapping line segment    # inspired by: http://pythonshort.blogspot.com/2015/03/intersection-of-two-line-segments-in.html    right = min(max(current_box[2], current_box[3]), max(neighbor_box[2], neighbor_box[3]))    left = max(min(current_box[2], current_box[3]), min(neighbor_box[2], neighbor_box[3]))    top = max(min(current_box[0], current_box[1]), min(neighbor_box[0], neighbor_box[1]))    bottom = min(max(current_box[0], current_box[1]), max(neighbor_box[0], neighbor_box[1]))    edge_segment = ((left, bottom), (right, top))    point_new = [0, 0]    # segment is vertical    if edge_segment[0][0] == edge_segment[1][0]:        point_new[0] = edge_segment[0][0]        edge_max = max(edge_segment[0][1], edge_segment[1][1])        edge_min = min(edge_segment[0][1], edge_segment[1][1])        # assign y axis        if point_cur[0] > edge_max:            point_new[1] = edge_max        elif point_cur[0] < edge_min:            point_new[1] = edge_min        else:            point_new[1] = point_cur[0]    # else segment is horizontal    else:        point_new[1] = edge_segment[0][1]        edge_max = max(edge_segment[0][0], edge_segment[1][0])        edge_min = min(edge_segment[0][0], edge_segment[1][0])        # assign y axis        if point_cur[1] > edge_max:            point_new[0] = edge_max        elif point_cur[1] < edge_min:            point_new[0] = edge_min        else:            point_new[0] = point_cur[1]    point_new = (point_new[1], point_new[0])    return point_new