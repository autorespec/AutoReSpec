public class TokenTest02 {

    //@ requires sentence != null;
    //@ requires sentence.length() > 0;
    //@ ensures \result ==> (sentence.split(" ").length > 3 && sentence.split(" ")[3].equals("generation"));
    //@ ensures !\result ==> (sentence.split(" ").length <= 3 || !sentence.split(" ")[3].equals("generation"));
    public static boolean f(String sentence) {
        String[] tokens = sentence.split(" ");
        
        int i = 0;
        //@ loop_invariant 0 <= i && i <= tokens.length;
        //@ loop_invariant i <= 3 || (i > 3 && tokens[3].equals("generation"));
        //@ decreases tokens.length - i;
        while (i < tokens.length) {
            if (i == 3) {
                if (!tokens[i].equals("generation")) {
                    return false;
                }
            }
            i++;
        }
        return tokens.length > 3;
    }
}