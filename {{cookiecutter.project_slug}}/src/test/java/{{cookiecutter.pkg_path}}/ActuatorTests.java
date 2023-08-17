package {{cookiecutter.pkg_name}};

import static io.restassured.RestAssured.get;
import static org.hamcrest.Matchers.equalTo;
import static org.hamcrest.Matchers.notNullValue;

import io.restassured.RestAssured;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.web.server.LocalServerPort;
import org.springframework.context.annotation.Import;
import org.springframework.test.context.ActiveProfiles;

@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@ActiveProfiles("test")
{% if cookiecutter.cache_type != 'none' -%}
@Import(JRedisMockConfiguration.class)
{%- endif %}
class ActuatorTests {

    @LocalServerPort int port;

    @BeforeEach
    public void setup() {
        RestAssured.baseURI = "http://localhost";
        RestAssured.port = port;
    }

    @Test
    void testHealthEndpoint() {
        // jedis-mock doesn't return a property for redis_version
        // thus actuator health endpoint will consider it down thus
        // mark the application as DOWN
        // we only test for livenessState until that issue is fixed
        get("/actuator/health")
                .then()
                .body("components.livenessState.status", equalTo("UP"));
    }

    @Test
    void testInfoEndpoint() {
        // this test requires the maven plugin to generate correct git information
        // if the test fails in IDE, just run mvn test once to ensure the git.properties
        // is generated under target/classes directory
        get("/actuator/info")
                .then()
                .body("app.name", notNullValue());
        get("/actuator/info")
                .then()
                .body("git.commit", notNullValue());
    }
}