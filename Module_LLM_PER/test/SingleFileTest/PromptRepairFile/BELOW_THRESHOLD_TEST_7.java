import java.util.*;

public class BELOW_THRESHOLD_TEST_7 {
  public static boolean below_threshold(int[] l, int t) {
    for (int i = 0; i < l.length; i++) {
      if (l[i] <= t) {
        return true;
      }
    }
    return false;
  }
}
