public static ArrayList<ArrayList> subsequences(int a, int b, int k) {
    if (k == 0) {
        // buggy code
        // return new ArrayList();
        <FILL_ME>
    }

    ArrayList ret = new ArrayList(50);
    for (int i=a; i<b+1-k; i++) {
        ArrayList base = new ArrayList(50);
        for (ArrayList rest : subsequences(i+1, b, k-1)) {
            rest.add(0,i);
            base.add(rest);
        }
        ret.addAll(base);

    }

    return ret;
}
