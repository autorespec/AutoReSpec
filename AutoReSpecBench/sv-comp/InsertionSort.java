public class InsertionSort {

  public static void sort(int[] a) {
    final int N = a.length;
    for (int i = 1; i < N; i++) { // N branches
      int j = i - 1;
      int x = a[i];
      // First branch (j >= 0):  2 + 3 + ... + N = N(N+1)/2 - 1 branches
      // Second branch (a[j] > x):  1 + 2 + ... + N-1 = (N-1)N/2 branches
      while ((j >= 0) && (a[j] > x)) {
        a[j + 1] = a[j];
        j--;
      }
      a[j + 1] = x;
    }
  }

}
