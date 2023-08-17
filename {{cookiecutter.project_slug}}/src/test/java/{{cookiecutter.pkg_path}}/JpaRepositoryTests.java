package {{cookiecutter.pkg_name}};

import static org.junit.jupiter.api.Assertions.assertEquals;

import {{cookiecutter.pkg_name}}.data.repository.CustomerRepository;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.ActiveProfiles;

@SpringBootTest
@ActiveProfiles("test")
class JpaRepositoryTests {

    @Autowired CustomerRepository customerRepository;

    @Test
    void canReadCustomers() {
        var customers = customerRepository.findAll();
        assertEquals(1, customers.size());
        assertEquals("Top one percent", customers.get(0).getName());
    }
}
