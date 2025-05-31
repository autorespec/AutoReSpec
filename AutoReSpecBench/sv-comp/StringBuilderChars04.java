public class StringBuilderChars04 {
  public static boolean f(String arg) {
    StringBuilder buffer = new StringBuilder(arg);

    char[] charArray = new char[buffer.length()];
    buffer.getChars(0, buffer.length(), charArray, 0);

    int i = 0;
    for (char character : charArray) {
      System.out.print(character);
      if (character == buffer.charAt(i))
        return false;
      ++i;
    }
    return true;
  }
}
