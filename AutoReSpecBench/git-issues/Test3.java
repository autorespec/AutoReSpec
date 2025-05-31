public class Test3 {

    static String lengthBalancerAddingZeroes(String binary_str, int lengthDiff)
    {
        for (int i = 0; i < lengthDiff; i++)
        {
            binary_str = "0" + binary_str;
        }
        return binary_str;
    }

}
