package {{cookiecutter.pkg_name}};

import jakarta.annotation.PostConstruct;
import lombok.extern.java.Log;
import {{cookiecutter.pkg_name}}.data.model.CasaAccount;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.stereotype.Component;

@Component
@Log
public class MongoDBSeeder {

    private final MongoTemplate mongoTemplate;

    @Autowired
    public MongoDBSeeder(MongoTemplate mongoTemplate) {
        this.mongoTemplate = mongoTemplate;
    }

    @PostConstruct
    public void seed() {
        mongoTemplate.insert(
                CasaAccount.builder()
                        .schemaVer("1")
                        .accountId("123")
                        .customerId("111")
                        .currency("SGD")
                        .balance(1000.00)
                        .flags("internal flag1")
                        .build(),
                "casa_accounts");

        mongoTemplate.insert(
                CasaAccount.builder()
                        .schemaVer("1")
                        .accountId("124")
                        .customerId("111")
                        .currency("USD")
                        .balance(888.88)
                        .flags("internal flag2")
                        .build(),
                "casa_accounts");

        log.info("seed data loaded");
    }
}
