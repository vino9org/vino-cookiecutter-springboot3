package {{cookiecutter.pkg_name}}.config;

import org.modelmapper.ModelMapper;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class BeanMapperConfiguration {
    @Bean
    public ModelMapper createModelMapper() {
        var mapper = new ModelMapper();
        mapper.getConfiguration().setAmbiguityIgnored(true);
        // additional configuration goes here
        return mapper;
    }
}