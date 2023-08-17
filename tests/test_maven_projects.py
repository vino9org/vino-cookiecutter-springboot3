import os
import random

from utils import (
    enumerate_features,
    run_build_in_generated_project,
    verify_generated_project,
)


def feature_selecter(api_type, database_type, cache_type, gen_k8s_yaml, qa_tools):
    if os.environ.get("TEST_ALL_FEATURES", "N") == "Y":
        # paranoid mode, insists on testing all features
        return True

    # each feature is independent
    # selectively test a few features by default to save time
    if (api_type, database_type, cache_type, gen_k8s_yaml, qa_tools) in [
        ("graphql", "postgresql", "redis", "no", ["spotless", "archunit"]),
        ("graphql", "none", "redis", "yes", ["spotless", "archunit"]),
        ("rest", "mysql", "none", "no", ["spotless", "archunit"]),
        ("rest", "mongodb", "none", "no", ["spotless", "archunit"]),
    ]:
        return True

    return False


def feature_id(api_type, database_type, cache_type, gen_k8s_yaml, qa_tools):
    return f"{api_type}-{database_type}-{cache_type}-{gen_k8s_yaml}-{'-'.join(qa_tools)}"


def pytest_generate_tests(metafunc):
    """dynamically generate test cases based on content of cookiecutter.json"""
    if "generator_ctx" in metafunc.fixturenames:
        keys = ["api_type", "database_type", "cache_type", "gen_k8s_yaml", "qa_tools"]
        features_to_test = enumerate_features(keys, feature_selecter)

        metafunc.parametrize(
            "generator_ctx",
            features_to_test,
            ids=[feature_id(**kw) for kw in features_to_test],
        )


def test_generate_and_build(cookies, generator_ctx):
    suffix = str(random.randint(1, 1000))
    result = cookies.bake(
        extra_context={
            "project_name": f"My Test Service {suffix}",
            "pkg_name": f"test.cookiecutter.svc{suffix}",
            "maven_version": f"1.0.{suffix}-SNAPSHOT",
            "api_type": generator_ctx["api_type"],
            "database_type": generator_ctx["database_type"],
            "cache_type": generator_ctx["cache_type"],
            "gen_k8s_yaml": generator_ctx["gen_k8s_yaml"],
            "qa_tools": generator_ctx["qa_tools"],
        }
    )
    assert verify_generated_project(result) is not None

    # shortcut to speed up dev and debug
    if os.environ.get("SKIP_MAVEN_TESTS", "N").upper() != "Y":
        assert run_build_in_generated_project(result.project_path)
