import itertools
import json
import os
import os.path
import shlex
import subprocess
import traceback

import yaml


def is_valid_yaml_file(yaml_file_path):
    try:
        with open(yaml_file_path, "r") as file:
            return yaml.safe_load_all(file)
    except yaml.YAMLError as exc:
        traceback.print_exception(exc)
        return None


def enumerate_features(keys, feature_filter):
    """
    read parameters from cookiecutter.json and generate all possible combinations
    return the list of dict after filtering out invalid entries
    """
    ctx_file = os.path.dirname(os.path.abspath(__file__)) + "/../cookiecutter.json"

    with open(ctx_file) as f:
        ctx = json.load(f)
        param_lists = [ctx[key] for key in keys]
        all_entries = [dict(zip(keys, val)) for val in itertools.product(*param_lists)]
        return [entry for entry in all_entries if feature_filter(**entry)]


def verify_generated_project(bake_result):
    if bake_result.exit_code != 0:
        print("===exception===")
        traceback.print_exception(bake_result.exception)
        print("===traceback===")
        traceback.print_tb(bake_result.exception.__traceback__)

    assert bake_result.exit_code == 0 and bake_result.exception is None
    assert bake_result.project_path.is_dir()
    assert (bake_result.project_path / ".git/HEAD").is_file()
    assert is_valid_yaml_file(bake_result.project_path / "src/main/resources/application.yml")

    return bake_result.project_path.name


def mvn_cmd():
    mvn = "./mvnw"

    # this setting is intended to be used in Github Actions
    if (
        os.path.exists("settings.xml")
        and os.environ.get("GITHUB_USER", "") != ""
        and os.environ.get("GITHUB_TOKEN", "") != ""
    ):
        # use local settings.xml when running in CI
        mvn += " --batch-mode -s settings.xml "

    return mvn


def run_build_in_generated_project(project_path):
    prev_cwd = os.getcwd()

    if os.path.isdir(project_path):
        os.chdir(project_path)
        print(f"running maven build for {os.path.basename(project_path)} ...")

        mvn = mvn_cmd()

        if (
            subprocess.call(shlex.split(f"{mvn} dependency:resolve")) == 0
            and subprocess.call(shlex.split(f"{mvn} dependency:resolve-plugins")) == 0
            and subprocess.call(shlex.split(f"{mvn} clean test")) == 0
        ):
            os.chdir(prev_cwd)
            return True

    os.chdir(prev_cwd)
    return False


def run_qa_plugins(project_path):
    prev_cwd = os.getcwd()

    if os.path.isdir(project_path):
        os.chdir(project_path)
        print(f"running QA plugins for {os.path.basename(project_path)} ...")

        mvn = mvn_cmd()

        # running sonar requires a running sonarqube server to work
        # to make it optional by setting RUN_SONAR
        if os.environ.get("RUN_SONAR", "N").upper() == "Y":
            sonar_cmd = f"{mvn} sonar:sonar -Dsonar:sonar -Dsonar.host.url=http://localhost:9000 "
            sonar_cmd += "-Dsonar.login=admin -Dsonar.password=password"
        else:
            sonar_cmd = "pwd"

        if (
            subprocess.call(shlex.split(f"{mvn} spotless:apply")) == 0
            and subprocess.call(shlex.split(f"{mvn} jqassistant:scan")) == 0
            and subprocess.call(shlex.split(sonar_cmd)) == 0
        ):
            os.chdir(prev_cwd)
            return True

    os.chdir(prev_cwd)
    return False
