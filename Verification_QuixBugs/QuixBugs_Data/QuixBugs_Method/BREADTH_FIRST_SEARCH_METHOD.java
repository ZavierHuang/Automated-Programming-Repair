public static Set<Node> nodesvisited = new HashSet<>();

public static boolean breadth_first_search(Node startnode, Node goalnode) {
    Deque<Node> queue = new ArrayDeque<>();
    queue.addLast(startnode);

    nodesvisited.add(startnode);
    // buggy code
    // while (true) {
    <FILL_ME>
        Node node = queue.removeFirst();

        if (node == goalnode) {
            return true;
        } else {
            for (Node successor_node : node.getSuccessors()) {
                if (!nodesvisited.contains(successor_node)) {
                    queue.addFirst(successor_node);
                    nodesvisited.add(successor_node);
                }
            }
        }
    }
    // buggy code
    <FILL_ME>
}

