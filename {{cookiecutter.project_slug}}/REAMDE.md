# Dummy microservice for testing only

This module is for testing the dependencies and configurations in [parent POM](../vino-svc-parent/pom.xml) are (mostly) correct.
This module only uses WebMVC and does not contain any elements for Reactive Web components.

## Use Spotless plugin to format code
```bash

# check if code is formatted
./mvnw spotless:check

# automatically apply default formatting
./mvnw spotless:apply


```

## Use jqassistant to analyze code structure
Before running the jqassistant plugin, make sure to update the following files to project specific configuration and rules.
* ```.jqassistant.yml``` configuration
* ```jqassistant/my-project.adoc```  rules


```bash
# ./mvn/jvm.config contains the configuration to run jqassistant

./mvnw jqassistant:scan

# if the result is written to embedded neo4j, run the server to explore the result
./mvnw jqassistant:server
```

## run sonarqube scanner
```bash
# adjust credentials and url accordingly
./mvnw sonar:sonar -Dsonar.host.url=http://localhost:9000 -Dsonar.login=username -Dsonar.password=password

```

## archunit
Archunit test rules are configured in parent pom and are automated executed during test execution. 


## Known issues
1. unit test fails due to ```libcrypto.so.1.1``` cannot be loaded when running on Ubuntu 22.04. The workaround has been added as a Maven profile ```ubuntu22``` in ```vino-demo-svc/pom.xml```. Activating it when override the OS detection so that correct Mongo binary is downloaded. 
```bash

   ./mvnw clean install -Pubuntu22

```
