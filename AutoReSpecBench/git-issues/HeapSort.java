public class HeapSort {

    public static void heapify(int /*@ non_null @*/ [] arr, final int i, final int len) {
        int j = i;

        while (true) {
            int m = j;
            if (m <= len/2) {
                int c = 2*m;
                if (arr[c-1] < arr[m-1]) m=c;
                if (c < len && arr[c] < arr[m-1]) m=c+1;
            }

            if (m==j) break;
            int tmp = arr[j-1];
            arr[j-1] = arr[m-1];
            arr[m-1] = tmp;
            j = m;
        }
    }
	

    public static void sort(int  [] arr) {
        if (arr.length < 2) return;


        for (int i = arr.length/2; i > 0; i--) {
            heapify(arr,i,arr.length);
        }


        int tmp;

        for (int len = arr.length-1; len>1; len--) {
            tmp = arr[0];
            arr[0] = arr[len];
            arr[len] = tmp;
            heapify(arr,1,len);
        }
        tmp = arr[0];
        arr[0] = arr[1];
        arr[1] = tmp;
    }

}