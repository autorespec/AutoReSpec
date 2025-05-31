
import java.util.Map;
import java.util.Collections;
import java.util.HashMap;

public final class B {

    private final Map<String, String> context;

    public B(Builder builder) {

        this.context = builder.context;

    }


    public void testMethodA()
    {
        System.out.println("Context: " + context);

    }


    public void testMethodB(Builder builder)
    {
        System.out.println("Passed Builder Context: " + builder.context);

    }

    public static class Builder {

        private Map<String, String> context = Collections.emptyMap();


        public Builder() {
        }


    }

}