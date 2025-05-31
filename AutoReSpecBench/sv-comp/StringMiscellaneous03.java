public class StringMiscellaneous03 {
  public static boolean f(String s1, String s2) {
    int i = 0;
    for (int count = s1.length() - 1; count >= 0; count--) {
      if (s1.charAt(count) == s2.charAt(i))
        return false;
      ++i;
    }
    return true;
  }
}
