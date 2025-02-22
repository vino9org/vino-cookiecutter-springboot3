package {{cookiecutter.pkg_name}}.test;

import static org.hamcrest.MatcherAssert.assertThat;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import {{cookiecutter.pkg_name}}.JRedisMockConfiguration;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.context.annotation.Import;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.web.client.RestTemplate;

@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@ActiveProfiles("test")
@AutoConfigureMockMvc
{% if cookiecutter.cache_type != 'none' -%}
@Import(JRedisMockConfiguration.class)
{%- endif %}
class CachedServiceTests {

    @Autowired MockMvc mockMvc;

    @Test
    void testCacheableWorks() throws Exception {
        var template = new RestTemplate();
        var ts0 = System.currentTimeMillis();

        mockMvc.perform(get("/rest/slow")).andExpect(status().is2xxSuccessful());
        var ts1 = System.currentTimeMillis();

        mockMvc.perform(get("/rest/slow")).andExpect(status().is2xxSuccessful());
        var ts2 = System.currentTimeMillis();

        // invoke api for the 1st time, should be slow
        assertThat("first call returns too soon", (ts1 - ts0) > 900);
        // invoke api for the 1st time, should be slow
        assertThat("second call returns too slow", (ts2 - ts1) < 100);
    }
}
