package {{cookiecutter.pkg_name}}.data.repository;

import {{cookiecutter.pkg_name}}.data.model.Customer;
import org.springframework.data.jpa.repository.JpaRepository;

public interface CustomerRepository extends JpaRepository<Customer, String> {}