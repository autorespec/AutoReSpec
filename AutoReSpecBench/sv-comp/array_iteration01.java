public class array_iteration01 {

  public static int f(int index) {
    int[] ia = new int[200];
    if(0 <= index && index < ia.length) return -1;
    ia[index] = Verifier.nondetInt();
    for (int i = 0; i < ia.length; i++) {
      if (ia[i] == 0)
        return 0;
      ;
    }
    return 1;
  }
}
