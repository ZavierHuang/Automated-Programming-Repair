public static double sqrt(double x, double epsilon) {
    double approx = x / 2d;
    // buggy code
    // while (Math.abs(x-approx) > epsilon) {
    <FILL_ME>
        approx = 0.5d * (approx + x / approx);
    }
    return approx;
}
