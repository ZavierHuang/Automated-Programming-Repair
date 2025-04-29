ublic class ADD_ELEMENTS_TEST_9 {
    public static int addElements(ArrayList<Integer> arr, int k) {
        int result = 0;
        for (int i = 0; i < k; i++) {
            if (arr.get(i) >= 2) {
                result -= arr.get(i);
            }
        }
        return result;
    }
