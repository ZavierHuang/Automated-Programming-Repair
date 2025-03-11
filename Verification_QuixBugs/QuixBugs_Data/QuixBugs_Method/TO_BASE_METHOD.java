public static String to_base(int num, int b) {
    String result = "";
    String alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    int i;
    while (num > 0) {
        i = num % b;
        num = num / b;
        // buggy code 
        // result = result + String.valueOf(alphabet.charAt(i));
        <FILL_ME>
    }

    return result;
}
