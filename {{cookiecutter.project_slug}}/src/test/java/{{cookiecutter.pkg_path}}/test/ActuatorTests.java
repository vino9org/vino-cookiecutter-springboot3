package {{cookiecutter.pkg_name}}.test;

// mess around with import order may potentially throw off the template import in cookiecutter
// spotless:off
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import {{cookiecutter.pkg_name}}.JRedisMockConfiguration;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.context.annotation.Import;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.web.servlet.MockMvc;

// spotless:on

@SpringBootTest()
@AutoConfigureMockMvc
@ActiveProfiles("test")
{% if cookiecutter.cache_type != 'none' -%}
@Import(JRedisMockConfiguration.class)
{%- endif %}
class ActuatorTests {

    @Autowired MockMvc mockMvc;

    @Test
    void testHealthEndpoint() throws Exception {
        // jedis-mock doesn't return a property for redis_version
        // thus actuator health endpoint will consider it down thus
        // mark the application as DOWN
        // we only test for livenessState until that issue is fixed
        mockMvc.perform(get("/actuator/health"))
                .andExpect(jsonPath("$.components.livenessState.status").value("UP"));
    }

    @Test
    void testInfoEndpoint() throws Exception {
        // this test requires the maven plugin to generate correct git information
        // if the test fails in IDE, just run mvn test once to ensure the git.properties
        // is generated under target/classes directory
        mockMvc.perform(get("/actuator/info"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.app.name").exists())
                .andExpect(jsonPath("$.git.commit").exists());
    }
}