public class NonNull {

    public class A {
        private String s;

        public A() {
            s = "hello";
        }
    }

    public class B {
        public B(A a) {
        }

        public void testMethod(A a) {
        }
    }

}
