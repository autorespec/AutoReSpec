public class Trie {
  private static final int R = 256; // extended ASCII

  private Node root; // root of trie
  private int N = 0; // number of keys in trie

  // R-way trie node
  private static class Node {
    private int val = -1;
    private Node[] next = new Node[R];
  }

  private static class CharArray {
    private int length = 0;
    public char[] array;
    private static final int DEFAULT_LENGTH = 42;

    public CharArray() {
      this(DEFAULT_LENGTH);
    }

    public CharArray(int length) {
      this.length = length;
      array = new char[length];
    }

    public int length() {
      return length;
    }

    public void set(int i, char c) {
      if (i < length) array[i] = c;
      else throw new ArrayIndexOutOfBoundsException("Error while setting char!");
    }

    public char get(int i) {
      if (i < length) return array[i];
      else throw new ArrayIndexOutOfBoundsException("Error while getting char!");
    }

    public CharArray substring(int start, int end) {
      int subLength = end - start;
      CharArray substr = new CharArray(subLength);
      for (int i = 0; i < subLength; i++) substr.set(i, this.get(i));
      return substr;
    }
  }

  public int get(CharArray key) {
    Node x = get2(root, key, 0);
    if (x == null) return -1;
    return x.val;
  }

  public boolean contains(CharArray key) {
    return get(key) != -1;
  }

  private Node get2(Node x, CharArray key, int d) {
    if (x == null) return null;
    if (d == key.length()) return x;
    char c = key.get(d);
    return get2(x.next[c], key, d + 1);
  }

  public void put(CharArray key, int val) {
    if (val == -1) delete(key);
    else root = put2(root, key, val, 0);
  }

  private Node put2(Node x, CharArray key, int val, int d) {
    if (x == null) x = new Node();
    if (d == key.length()) {
      if (x.val == -1) N++;
      x.val = val;
      return x;
    }

    char c = key.get(d);
    x.next[c] = put2(x.next[c], key, val, d + 1);
    return x;
  }

  public int size() {
    return N;
  }

  public boolean isEmpty() {
    return size() == 0;
  }

  public CharArray longestPrefixOf(CharArray query) {
    int length = longestPrefixOf(root, query, 0, -1);
    if (length == -1) return null;
    else return query.substring(0, length);
  }

  private int longestPrefixOf(Node x, CharArray query, int d, int length) {
    if (x == null) return length;
    if (x.val != -1) length = d;
    if (d == query.length()) return length;
    char c = query.get(d);
    return longestPrefixOf(x.next[c], query, d + 1, length);
  }

  public void delete(CharArray key) {
    root = delete(root, key, 0);
  }

  private Node delete(Node x, CharArray key, int d) {
    if (x == null) return null;
    if (d == key.length()) {
      if (x.val != -1) N--;
      x.val = -1;
    } else {
      char c = key.get(d);
      x.next[c] = delete(x.next[c], key, d + 1);
    }

    // remove subtrie rooted at x if it is completely empty
    if (x.val != -1) return x;
    for (int c = 0; c < R; c++) if (x.next[c] != null) return x;
    return null;
  }

}
