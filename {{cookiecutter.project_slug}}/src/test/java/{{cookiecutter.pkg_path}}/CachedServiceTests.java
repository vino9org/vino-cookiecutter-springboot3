package {{cookiecutter.pkg_name}};

import static org.hamcrest.MatcherAssert.assertThat;
import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.web.server.LocalServerPort;
import org.springframework.context.annotation.Import;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.web.client.RestTemplate;

@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@ActiveProfiles("test")
{% if cookiecutter.cache_type != 'none' -%}
@Import(JRedisMockConfiguration.class)
{%- endif %}
class CachedServiceTests {

    @LocalServerPort int port;

    @Test
    void testCacheableWorks() {
        var template = new RestTemplate();
        var ts0 = System.currentTimeMillis();

        var svcUrl = "http://localhost:" + port + "/rest/slow";

        assertTrue(template.getForEntity(svcUrl, String.class).getStatusCode().is2xxSuccessful());
        var ts1 = System.currentTimeMillis();

        assertTrue(template.getForEntity(svcUrl, String.class).getStatusCode().is2xxSuccessful());
        var ts2 = System.currentTimeMillis();

        // invoke api for the 1st time, should be slow
        assertThat("first call returns too soon", (ts1 - ts0) > 900);
        // invoke api for the 1st time, should be slow
        assertThat("second call returns too slow", (ts2 - ts1) < 100);
    }
}
