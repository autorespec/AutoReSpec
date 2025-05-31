public class AmountSeq{

    private int cents;

    private int euros;


    public Amount(int euros, int cents){
        this.euros = euros;
        this.cents = cents;
    }

    public Amount negate(){
        return new Amount(-euros,-cents);
    }

}