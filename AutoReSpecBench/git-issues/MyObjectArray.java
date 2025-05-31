public class MyObjectArray {

    public class Address {
        public int address;

        public Address(int address) {
            this.address = address;
        }
    }


    public Address[] addresses = new Address[100];



    public MyObjectArray() {

        for (int i = 0; i < 100; ++i) {
            addresses[i] = new Address(88);
        }


        for (int i = 0; i < 100; ++i) {
            addresses[i].address = 99;
        }
    }

}