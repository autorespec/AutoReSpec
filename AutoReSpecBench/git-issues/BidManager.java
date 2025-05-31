public class BidManager {

    public BidArray[][] bidArrays = new BidArray[1000][1000];

    public BidManager() {
        for (int i = 0; i < 1000; ++i) {
            for (int j = 0; j < 1000; ++j) {
                bidArrays[i][j] = new BidArray();
            }
        }
    }

    public void push() {
        bidArrays[0][0].push(new Bid(1, 2));
    }

    // Dummy classes for compilation
    public static class Bid {
        int id, value;

        public Bid(int id, int value) {
            this.id = id;
            this.value = value;
        }
    }

    public static class BidArray {
        public void push(Bid bid) {
            System.out.println("Pushed bid: id=" + bid.id + ", value=" + bid.value);
        }
    }

    public static void main(String[] args) {
        BidManager manager = new BidManager();
        manager.push(); // Test the push
    }
}
