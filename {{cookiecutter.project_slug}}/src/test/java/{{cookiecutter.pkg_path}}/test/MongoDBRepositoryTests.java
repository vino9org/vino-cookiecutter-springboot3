package {{cookiecutter.pkg_name}}.test;

import static org.junit.jupiter.api.Assertions.assertEquals;

import {{cookiecutter.pkg_name}}.data.repository.CasaAccountRepository;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.ActiveProfiles;

@SpringBootTest
@ActiveProfiles("test")
class MongoDBRepositoryTests {

    @Autowired CasaAccountRepository accountRepository;

    @Test
    void canReadAccounts() {
        var accounts = accountRepository.findAll();
        assertEquals(2, accounts.size());
        assertEquals("111", accounts.get(0).getCustomerId());
    }
}
