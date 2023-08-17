package {{cookiecutter.pkg_name}}.api.rest;

import org.springframework.cache.annotation.Cacheable;
import org.springframework.stereotype.Component;

@Component
public class SlowService {

    // the logic is deliberately slow for testing of the @Cacheable annotation
    @Cacheable("default")
    @java.lang.SuppressWarnings("java:S2142")
    public String randLong() {
        try {
            Thread.sleep(1000L);
        } catch (InterruptedException e) {
            // do nothing
        }
        var nnn = Math.round(Math.random() * 100000.00);
        return String.valueOf(nnn);
    }
}