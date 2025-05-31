public class Block {
    private int[] contents;


    public Block() { contents = new int[10]; }


    public Block(int[] cont) {
        contents = cont;
    }


    public static Block allocate(int size) {
        int[] cont = new int[size];
        return new Block(cont);
    }

}