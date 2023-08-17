package {{cookiecutter.pkg_name}}.data.model;

import static jakarta.persistence.GenerationType.IDENTITY;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import lombok.Getter;
import lombok.NoArgsConstructor;

@Entity
@NoArgsConstructor
@Getter
@Table(name = "customers")
public class Customer {
    @Id
    @GeneratedValue(strategy = IDENTITY)
    Long id;

    String customerId;
    String name;
    CustomerStatus status;
}

enum CustomerStatus {
    ACTIVE,
    INACTIVE
}
