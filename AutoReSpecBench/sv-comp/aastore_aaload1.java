import java.util.Random;

public class aastore_aaload1 {
  static class A {
    int value = 0;
  }

  public static void main(String[] args) {
    int size = new Random().nextInt();
    if (size < 0) return;
    A[] array = new A[size];

    for (int i = 0; i < size; i++) {
      array[i] = new A();
    }
    for (int i = 0; i < size; i++) {
      assert array[i] != null;
    }
  }
}
