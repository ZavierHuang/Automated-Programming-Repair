
        import java.util.*;
        public class BELOW_THRESHOLD_TEST_7 {
                public static boolean below_threshold(int[] l, int t) {
        for (int i = 0; i < l.length; i += 1) {
// buggy code
//             if (l[i] <= t)
//                 return true;
//         }
//         return false;
            if (l[i] <= t)
                return true;
        }
        return false;
    }
    }

            
        }
        