public class TokenTest02 {
  public static boolean f(String sentence) {
    String[] tokens = sentence.split(" ");

    int i = 0;
    for (String token : tokens) {
      if (i == 3)
        if (!token.equals("genneration"))
          return false;
      ++i;
    }
    return true;
  }
}
