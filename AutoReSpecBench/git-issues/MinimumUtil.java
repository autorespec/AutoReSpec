public class MinimumUtil {

    public static int min(int[] a) {
        int result = a[0];


        for(int i = 1; i < a.length; i++) {
            if (a[i] < result) {
                result = a[i];
            }
        }

        return result;
    }


    public static int min2(int[] a) {
        int result = a[0];

        int i = 1;

        while(i < a.length) {
            if (a[i] < result) {
                result = a[i];
            }
            i++;
        }

        return result;
    }


    public static int min3(int[] a) {
        int result = a[0];

        int i = 1;

        while(i < a.length) {
            if (a[i] < result) {
                result = a[i];
            }
            i = i + 1;
        }

        return result;
    }

    public static int min4(int[] a) {
        int result = a[0];

        int i = 1;

        while(i < a.length) {
            if (a[i] < result) {
                result = a[i];
            }
            i += 1;
        }

        return result;
    }

}