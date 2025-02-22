import os

from utils import run_build_in_generated_project, verify_generated_project

from tests.utils import run_qa_plugins


def test_generate_and_build_one_project(cookies):
    result = cookies.bake(
        extra_context={
            "project_name": "My Test Service",
            "pkg_name": "test.cookiecutter.svc",
            "maven_version": "1.0.0-SNAPSHOT",
            "api_type": "graphql",
            "database_type": "postgresql",
            "cache_type": "redis",
            "gen_k8s_yaml": "yes",
            "use_github_action": "yes",
            "qa_tools": ["spotless", "archunit", "jqassistant"],
        }
    )
    print(result)
    print(result.exception)
    assert verify_generated_project(result) == "my-test-service"
    assert os.path.exists(result.project_path / "k8s/base/kustomization.yaml")
    assert os.path.exists(result.project_path / ".github/workflows/jib_build.yaml")

    if os.environ.get("SKIP_MAVEN_TESTS", "N") != "Y":
        run_build_in_generated_project(result.project_path)

    run_qa_plugins(result.project_path)

    print("project gernated in\n")
    print(result.project_path)


def test_generate_no_optional_files(cookies):
    result = cookies.bake(
        extra_context={
            "project_name": "My Simple Service",
            "pkg_name": "test.cookiecutter.svc_simple_1",
            "maven_version": "1.0.0-SNAPSHOT",
            "api_type": "rest",
            "database_type": "none",
            "cache_type": "none",
            "gen_k8s_yaml": "no",
            "use_github_action": "no",
            "qa_tools": ["spotless"],
        }
    )
    assert verify_generated_project(result) == "my-simple-service"
    assert not os.path.exists(result.project_path / "k8s")
    assert not os.path.exists(result.project_path / ".github")
    assert not os.path.exists(result.project_path / "jqassistant")
