public static boolean detect_cycle(Node node) {
    Node hare = node;
    Node tortoise = node;

    while (true) {
        // buggy code
        // if (hare.getSuccessor() == null)
        <FILL_ME>
            return false;

        tortoise = tortoise.getSuccessor();
        hare = hare.getSuccessor().getSuccessor();

        if (hare == tortoise)
            return true;
    }
}
