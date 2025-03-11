public static int bitcount(int n) {
    int count = 0;
    while (n != 0) {
        // buggy code
        // n = (n ^ (n - 1));
        <FILL_ME>
        count++;
    }
    return count;
}
