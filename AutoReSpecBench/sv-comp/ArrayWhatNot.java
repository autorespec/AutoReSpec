class ArrayWhatNot {

  class what_not {
  };

  public static int func(int size) {
    if (size < 8) return -1;

    int int_array[] = new int[size];

    for (int i = 0; i < size; i++)
      int_array[i] = i;

    if (int_array[7] != 7)
      return 0;

    what_not what_not_array[] = new what_not[size];

    if (what_not_array.length != size)
      return 0;
    return 1;
  }
}
