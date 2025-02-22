package {{cookiecutter.pkg_name}}.test;

import static org.assertj.core.api.Assertions.assertThat;

import com.netflix.graphql.dgs.DgsQueryExecutor;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.ActiveProfiles;

@SpringBootTest
@ActiveProfiles("test")
class GraphQLQueryTests {
    @Autowired DgsQueryExecutor dgsQueryExecutor;

    @Test
    void test_get_account_details() {
        var query =
                """
                {
                    CasaAccount(accountId: "123") {
                    accountId
                    balance
                    currency
                    }
                }
                """;

        var result = dgsQueryExecutor.executeAndGetDocumentContext(query);

        String accountId = result.read("data.CasaAccount.accountId");
        assertThat(accountId).isEqualTo("123");
    }
}
