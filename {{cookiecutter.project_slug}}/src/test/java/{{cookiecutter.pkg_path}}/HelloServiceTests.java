package {{cookiecutter.pkg_name}};

import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.web.server.LocalServerPort;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.web.client.RestTemplate;

@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@ActiveProfiles("test")
class HelloServiceTests {

    @LocalServerPort int port;

    @Test
    void testHelloApi() {
        var template = new RestTemplate();
        var svcUrl = "http://localhost:" + port + "/rest/hello";

        assertTrue(template.getForEntity(svcUrl, String.class).getStatusCode().is2xxSuccessful());
    }
}