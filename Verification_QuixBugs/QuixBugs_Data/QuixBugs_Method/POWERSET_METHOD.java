public static ArrayList<ArrayList> powerset(ArrayList arr) {
    if (!arr.isEmpty()) {
        Object first = arr.get(0);
        arr.remove(0);
        ArrayList rest = arr;
        ArrayList<ArrayList> rest_subsets = powerset(rest);

        ArrayList<ArrayList> output = new ArrayList<ArrayList>(100);
        ArrayList to_add = new ArrayList(100);

        // buggy code
        // to_add.add(first);
        // for (ArrayList subset : rest_subsets) {
        //     to_add.addAll(subset);
        // }
        // output.add(to_add);
        // return output;
        <FILL_ME>
    } else {
        ArrayList empty_set = new ArrayList<ArrayList>();
        empty_set.add(new ArrayList());
        return empty_set;
    }
}