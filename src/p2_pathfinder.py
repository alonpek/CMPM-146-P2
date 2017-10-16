# Alon Pekurovsky# Dean Rabinowitz# NOT CONSTRUCTING CORRECT PATHfrom heapq import heappop, heappushimport numpydef find_path (source_point, destination_point, mesh):    """    Searches for a path from source_point to destination_point through the mesh    Args:        source_point: starting point of the pathfinder        destination_point: the ultimate goal the pathfinder must reach        mesh: pathway constraints the path adheres to    Returns:        A path (list of points) from source_point to destination_point if exists        A list of boxes explored by the algorithm    """    # Step 1: See method desc    start_box, dest_box = find_start_dest(source_point, destination_point, mesh)    # Step 2: Implement A*    queue = [(0, start_box)]    detail_points = {}    detail_points[start_box] = source_point    path = []    parent_box = {}    parent_box[start_box] = None    dist = {}    dist[start_box] = 0    found = False    while len(queue) != 0:        current_dist, current_box = heappop(queue)        if current_box == dest_box:            found = True            # construct the path            path = [destination_point]            path.append(detail_points[current_box])            # path = [detail_points[current_box]]            print(detail_points)            while parent_box[current_box] is not None:                path.append(detail_points[parent_box[current_box]])                current_box = parent_box[current_box]            path.append(source_point)            flip_path = path[::-1]            seg_path = zip(flip_path[:-1], flip_path[1:])            return seg_path, parent_box.keys()        # PROBLEM MUST BE HERE ----------------------------------------------------        for neighbor_box in mesh['adj'][current_box]:            current_point = detail_points[current_box]            next_point = get_next_point(current_box, neighbor_box, detail_points)            new_dist = dist[current_box] + get_dist(current_point, next_point)            # new_dist = dist[current_point] + get_dist(current_point, next_point)            if neighbor_box not in dist or new_dist < dist[neighbor_box]:                detail_points[neighbor_box] = next_point                dist[neighbor_box] = new_dist                queue_dist = new_dist + get_dist(next_point, destination_point)                heappush(queue, (queue_dist, neighbor_box))                parent_box[neighbor_box] = current_box            # ----------------------------------------------------------------------    if not found:        print('No path found!')    return path, parent_box.keys()def find_start_dest(source_point, destination_point, mesh):    """    Step 1: identify which boxes contain source and destination    """    for box in mesh['boxes']:        if box[3] >= source_point[1] >= box[2]:            if box[1] >= source_point[0] >= box[0]:                start_box = box        if box[3] >= destination_point[1] >= box[2]:            if box[1] >= destination_point[0] >= box[0]:                dest_box = box    return start_box, dest_boxdef get_dist(p1, p2):    """    Calculate the Euclidean distance between two tuples.    """    a = numpy.array(p1)    b = numpy.array(p2)    dist = numpy.sqrt(numpy.sum((a-b)**2))    return distdef get_next_point(current_box, neighbor_box, detail_points):    point_cur = detail_points[current_box]    # min of max and max of min idea to calculate overlapping line segment    # inspired by: http://pythonshort.blogspot.com/2015/03/intersection-of-two-line-segments-in.html    right = min(max(current_box[2], current_box[3]), max(neighbor_box[2], neighbor_box[3]))    left = max(min(current_box[2], current_box[3]), min(neighbor_box[2], neighbor_box[3]))    top = max(min(current_box[0], current_box[1]), min(neighbor_box[0], neighbor_box[1]))    bottom = min(max(current_box[0], current_box[1]), max(neighbor_box[0], neighbor_box[1]))    edge_segment = ((left, bottom), (right, top))    point_new = [0, 0]    # segment is vertical    if edge_segment[0][0] == edge_segment[1][0]:        point_new[0] = edge_segment[0][0]        edge_max = max(edge_segment[0][1], edge_segment[1][1])        edge_min = min(edge_segment[0][1], edge_segment[1][1])        # assign y axis        if point_cur[0] > edge_max:            point_new[1] = edge_max        elif point_cur[0] < edge_min:            point_new[1] = edge_min        else:            point_new[1] = point_cur[0]    # else segment is horizontal    else:        point_new[1] = edge_segment[0][1]        edge_max = max(edge_segment[0][0], edge_segment[1][0])        edge_min = min(edge_segment[0][0], edge_segment[1][0])        # assign y axis        if point_cur[1] > edge_max:            point_new[0] = edge_max        elif point_cur[1] < edge_min:            point_new[0] = edge_min        else:            point_new[0] = point_cur[1]    point_new = (point_new[1], point_new[0])    # detail_points[neighbor_box] = point_new    return point_new