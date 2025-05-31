class LinkedListEntry {
  public LinkedListEntry Next;
  public int Value;
}

class LinkedList {
  public LinkedListEntry Head;

  public int size() {
    int count = 0;
    for (LinkedListEntry entry = Head; entry != null; entry = entry.Next) ++count;
    return count;
  }

  public void add(int index, int e) {
    LinkedListEntry newEntry = new LinkedListEntry();
    newEntry.Value = e;
    if (index == 0) {
      Head = newEntry;
      return;
    }
    LinkedListEntry entry = Head;
    for (int i = 1; i < index; ++i) entry = entry.Next;
    entry.Next = newEntry;
  }

  public void add(int e) {
    add(size(), e);
  }

  public void remove(int index) {
    LinkedListEntry entry = Head;
    for (int i = 1; i < index; ++i) entry = entry.Next;
    entry.Next = entry.Next.Next;
  }

  public int get(int index) {
    LinkedListEntry entry = Head;
    for (int i = 0; i < index; ++i) entry = entry.Next;
    return entry.Value;
  }
}

class Utils_synthesis {
  public static int accumulator(int aggregated, int e) {
    if (e % 2 == 0) if (aggregated < e) return e;
    return aggregated;
  }

  public static boolean predicate(int lhs) {
    return true;
  }
}
