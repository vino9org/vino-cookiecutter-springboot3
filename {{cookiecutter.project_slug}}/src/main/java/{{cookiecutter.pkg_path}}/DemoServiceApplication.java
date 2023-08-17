package {{cookiecutter.pkg_name}};

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
{% if cookiecutter.cache_type != 'none' -%}
import org.springframework.cache.annotation.EnableCaching;
{% endif -%}
{% if cookiecutter.database_type == 'postgresql' or cookiecutter.database_type == 'mysql' -%}
import org.springframework.data.jpa.repository.config.EnableJpaRepositories;
{% endif -%}
{% if cookiecutter.database_type == 'mongodb' -%}
import org.springframework.data.mongodb.repository.config.EnableMongoRepositories;

{% endif -%}

@SpringBootApplication
{% if cookiecutter.database_type == 'mongodb' -%}
@EnableMongoRepositories
{% endif -%}
{% if cookiecutter.cache_type != 'none' -%}
@EnableCaching
{% endif -%}
{% if cookiecutter.database_type == 'postgresql' or cookiecutter.database_type == 'mysql' -%}
@EnableJpaRepositories
{% endif -%}
public class DemoServiceApplication {

    public static void main(String[] args) {
        SpringApplication.run(DemoServiceApplication.class, args);
    }
}