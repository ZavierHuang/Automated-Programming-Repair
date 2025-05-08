
public class BELOW_THRESHOLD_TEST_7 {
    public static boolean belowThreshold(int[] l, int t) {
        for (int i = 0; i < l.length; i += 1) {
            if (l[i] <= t) {
                return true;
            }
        }
        return false;
    }
}