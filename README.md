# Cookiecutter template for Spring Boot microservice

[![Built with Devbox](https://jetpack.io/img/devbox/shield_galaxy.svg)](https://jetpack.io/devbox/docs/contributor-quickstart/)

To use the template, please install cookiecutter on your computer by following [instructions here](https://cookiecutter.readthedocs.io/en/latest/installation.html)

```shell
# the code generated requires vino-svc-parent POM and library to work
# install it first

git clone https://github.com/vino9org/vino-java-base.git
cd vino-java-base
./mvnw install -DskipTests

# generate the code in interactive model
cookiecutter https://github.com/vino9org/vino-cookiecutter-springboot3


# generate code in batch mode with a config file

cat << 'EOF' > project.yaml
default_context:
    project_name: "my test svc"
EOF

cookiecutter --config-file project.yaml --no-input https://github.com/vino9org/vino-cookiecutter-springboot3

cd my-test-svc
./mvnw dependency:resolve
./mvnw clean test


```

## To do devleopment on this

[Poetry](https://python-poetry.org/) is recommended as package mangager for development in Python. The ```vino-demo-svc``` in [vino-base repo](https://github.com/vino9org/vino-base/vino-demo-svc) is the used for generating the template. First head over there, update the project and pass all unit tests, then

```shell
# use devbox (preferred)
devbox shell

# using poetry
poetry shell
poetry install

# or just use pip
pip install -r requirements-dev.txt

# copy java project into template directory
# the migration script is very limited and makes a lots of assumptions.
# most likely it won't work with other Java repo.
python migrate.py <path to vino-demo-svc>

# test and debug generation
# this will generate 1 projects and run all mvn command on it
# in order to test running with Sonar maven plugin, a sonar server must be running
# at http://localhost:9000 with credential admin:password
# please edit tests/tests_util.py if the url and credentials are different

pytest -s -k test_generate_and_build_one_project --keep-baked-projects

# run all tests

pytest -v

# all good? commit and push.

```

The ```--keep-baked-projects``` keeps the work directory of cookiecutter so it can be used for troubleshooting.
Ideally the fix should come from Java project or migrate.py. Manually patch the template works in a pintch, but
running migrate.py again will likely create the same problem again.

## TO DO
