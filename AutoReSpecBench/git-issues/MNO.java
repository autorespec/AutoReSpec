public class MNO {

    static class XYZ {

        private static void callMe() {
            throw new IndexOutOfBoundsException();
        }

        private static boolean convertException() {
            try {
                callMe();
            } catch (IndexOutOfBoundsException ex) {
                Object obj = ex;
                String s = obj.toString();
                Throwable th = ex;
                s = th.toString();
                throw new ArrayIndexOutOfBoundsException(s);
            }
            return true;
        }

}