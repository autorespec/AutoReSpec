public class AmountBranched {

    private int cents;
    private int euros;

    public AmountFixed(int euros, int cents) {
        int totalCents = euros * 100 + cents;
        this.euros = totalCents / 100;
        this.cents = totalCents % 100;
        if (this.cents < 0) {
            this.cents += 100;
            this.euros -= 1;
        }
    }

    public AmountFixed negate() {
        int totalCents = euros * 100 + cents;
        totalCents = -totalCents;
        return new AmountFixed(totalCents / 100, totalCents % 100);
    }
}
