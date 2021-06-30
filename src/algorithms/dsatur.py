from model.Graph import Graph


def saturation_degree(course: int, graph: Graph, colour_map: dict) -> int:
    used_colours = []
    for vertex in graph.get_neighbours(course):
        if colour_map[vertex] and colour_map[vertex] not in used_colours:
            used_colours.append(colour_map[vertex])
    return len(used_colours)


def uncoloured_neighbours_count(course: int, graph: Graph, colour_map: dict) -> int:
    degree = 0
    for vertex in graph.get_neighbours(course):
        degree += 1 if colour_map[vertex] == 0 else 0
    return degree


def degree_of_saturation_algorithm(graph: Graph) -> dict:
    queue = graph.get_vertices_degrees()
    colours_set = [i for i in range(1, 61)]
    max_colour = -1
    used_colours = []
    colours_map = {}
    for (course, _) in queue:
        colours_map[course] = 0
    while queue:
        (course, _) = queue.pop(0)
        # Try colouring with an already used colour
        for colour in used_colours:
            colours_map[course] = colour
            if graph.valid_colouring_for(course, colours_map):
                break
            colours_map[course] = 0 # Try next colour
        # If no existent colour can be used, then add a new one
        if colours_map[course] == 0:
            max_colour += 1
            used_colours.append(colours_set[max_colour])
            colours_map[course] = used_colours[-1]
        queue = sorted(
            queue,
            key=lambda course: (
                saturation_degree(course, graph, colours_map),
                uncoloured_neighbours_count(course, graph, colours_map)
            ),
            reverse=True
        )
    return colours_map
