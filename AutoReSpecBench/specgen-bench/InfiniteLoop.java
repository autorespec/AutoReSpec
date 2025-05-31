import java.util.Random;

public class InfiniteLoop {

  public static void infiniteLoop(String[] arg) {
    int i = 0;
    boolean b = new Random().nextBoolean();

    while (b) {
      i++;
    }
  }

}
