# migrate code from maven example project to a cookiecutter template
import os
import pathlib
import re
import shutil
import sys
import xml.etree.ElementTree as et

TEMPLATE_DIR = "{{cookiecutter.project_slug}}"

# files to be deleted after generation
to_delete_files = [
    "{% if cookiecutter.use_github_action != 'yes' %} .github/workflows/jib_build.yaml {% endif -%}",
    "{% if 'jqassistant' not in cookiecutter.qa_tools %} jqassistant/proj-rules.adoc {% endif %}",
]


comment_regex = {
    "java": (
        re.compile(r"(^\s*)//\s*CC:\s*(.*)$"),
        re.compile(r"(^\s*)//\s*DELETE_IF:\s*(.*)$"),
    ),
    "xml": (
        re.compile(r"^(\s*)<!--\s*CC:\s*(.*)\s*-->$"),
        re.compile(r"^(\s*)<!--\s*DELETE_IF:\s*(.*)\s*-->$"),
    ),
    "yaml": (
        re.compile(r"^(\s*)#\s*CC:\s*(.*)$"),
        re.compile(r"^(\s*)#\s*DELETE_IF:\s*(.*)$"),
    ),
    "sql": (
        re.compile(r"^(\s*)--\s*CC:\s*(.*)$"),
        re.compile(r"^(\s*)--\s*DELETE_IF:\s*(.*)$"),
    ),
}


class CommentedTreeBuilder(et.TreeBuilder):
    def comment(self, data):
        self.start(et.Comment, {})
        self.data(data)
        self.end(et.Comment)


def replace_pomxml_tag(root, tag_path, new_value) -> None:
    elem = root
    for tag in tag_path.split("/"):
        elem = elem.find("{http://maven.apache.org/POM/4.0.0}" + tag)
        if elem is None:
            print(f"cannot replace {tag_path} in pom.xml")
            return

    elem.text = new_value


def ensure_dir_exists(path: str) -> str:
    if not os.path.exists(path):
        pathlib.Path(path).mkdir(parents=True, exist_ok=True)
    return path


def detect_java_pkg(base_path: str) -> str:
    """
    detect the top level java package of a java project
    the first directory
    """
    java_module_name = os.path.basename(base_path)
    java_src_path = base_path + "/src/main/java"
    if not os.path.exists(java_src_path):
        return None

    for root, dirs, files in os.walk(java_src_path, topdown=True):
        # print("root=", root, "dirs=", dirs)
        if len(dirs) > 1:
            pkg = os.path.relpath(root, java_src_path).replace("/", ".")
            print(f"= detected java pacakage for module {java_module_name} is {pkg}")
            return java_module_name, pkg


def copy_maven_project(src_path: str, dst_base_path: str, source_java_path: str) -> str:
    """
    1. copy the maven project to a cookiecutter template directory,
       replace package path with {{cookiecutter.pkg_path}}.
    """
    dst_path = ensure_dir_exists(dst_base_path + "/" + TEMPLATE_DIR)
    shutil.rmtree(dst_path + "/src", ignore_errors=True)
    shutil.rmtree(dst_path + "/pom.xml", ignore_errors=True)

    for root, dirs, files in os.walk(src_path, topdown=True):
        for dd in ["target", ".mvn"]:
            if dd in dirs:
                dirs.remove(dd)

        for src_file in files:
            root_rel_path = os.path.relpath(root, src_path)
            output_path = dst_path + "/" + root_rel_path.replace(source_java_path, "{{cookiecutter.pkg_path}}")
            shutil.copy(root + "/" + src_file, ensure_dir_exists(output_path))

    return dst_path


def replace_java_pkg(file_path: str, source_java_pkg) -> None:
    """
    2. for each Java file, replace package name with {{cookiecutter.pkg_name}}
    """
    # TODO: skip comments
    with open(file_path, "r") as f:
        content = "".join(f.readlines())
        new_content = content.replace(source_java_pkg, "{{cookiecutter.pkg_name}}")
    with open(file_path, "w") as f:
        f.write(new_content)


def process_pomxml(file_path: str) -> None:
    """
    3. for pom.xml, replace groupId, artifactId etc with {{cookiecutter.*}}
    """
    et.register_namespace("", "http://maven.apache.org/POM/4.0.0")

    tree = et.parse(file_path, parser=et.XMLParser(target=CommentedTreeBuilder()))
    root = tree.getroot()
    replace_pomxml_tag(root, "groupId", "{{cookiecutter.maven_group_id}}")
    replace_pomxml_tag(root, "artifactId", "{{cookiecutter.maven_artifact_id}}")
    replace_pomxml_tag(root, "version", "{{cookiecutter.version}}")
    replace_pomxml_tag(root, "name", "{{cookiecutter.project_slug}}")
    replace_pomxml_tag(root, "description", "{{cookiecutter.project_short_description}}")
    replace_pomxml_tag(root, "parent/relativePath", "")
    replace_pomxml_tag(
        root,
        "properties/graphql.codegen.package",
        "{{cookiecutter.pkg_name ~ '.generated'}}",
    )

    tree.write(file_path, xml_declaration=True, encoding="utf-8")


def replace_slug_at_line_end(file_path: str, source_svc_name) -> None:
    """
    4. for each yaml/yml file, repalce app name at end of line wih {{cookiecutter.project_name}}
    """
    output = []
    with open(file_path, "r") as f:
        for line in f.readlines():
            line = line.rstrip()
            if len(line) > 5:
                # if the line ends with dummy slug, followed by single or double quote
                # treat it as a string that should be replaced
                if (
                    line.endswith(source_svc_name)
                    or line.endswith(source_svc_name + "'")
                    or line.endswith(source_svc_name + '"')
                ):
                    line = line.replace(source_svc_name, "{{cookiecutter.project_slug}}")
            output.append(line)
    with open(file_path, "w") as f:
        f.write("\n".join(output))


def process_comments(file_path: str) -> None:
    """
    5 & 6....

    process 2 types single line comments in source files

    CC: {jinja2 expression} -> simple remove comments and expose the jinja2 expression for code generation

    DELETE_IF: {jinjia2 expression} -> remove the comment line, and conslidate the expression and file names into
    to_delete.txt file which will be used by post_generate hook to delete the files. since cookiecutter doesn't have
    conditional file or directory generation so we will just delete them after generation.
    """
    global to_delete_files

    _, ext = os.path.splitext(file_path)
    if ext == ".java":
        re_comment, re_delif = comment_regex["java"]
    elif ext == ".xml":
        re_comment, re_delif = comment_regex["xml"]
    elif ext in [".yaml", ".yml", ".env", ".txt"]:
        re_comment, re_delif = comment_regex["yaml"]
    elif ext == ".sql":
        re_comment, re_delif = comment_regex["sql"]
    else:
        return

    output = []
    with open(file_path, "r") as f:
        for line in f.readlines():
            line = line.rstrip()

            try:
                match = re_delif.search(line)
                if match:
                    expr = match.group(2).strip()
                    # get the remaing part of the file_path after TEMPLATE_DIR
                    # this will be used to delete the file after generation
                    i = file_path.index(TEMPLATE_DIR) + len(TEMPLATE_DIR) + 1
                    rel_path = file_path[i:]
                    to_delete_files.append("{% if " + expr + " %} " + rel_path + "  {% endif %}")
                    continue

                match = re_comment.search(line)
                if match:
                    output.append(match.group(1) + match.group(2))
                    continue
            except re.error:
                print(f"cannot parse {line}")

            output.append(line)

    with open(file_path, "w") as f:
        f.write("\n".join(output))


def migrate(base_path: str, output_path: str) -> None:
    """
    Over process of migrating a maven project to a cookiecutter template
    1. copy the maven project to a cookiecutter template directory, replace package path with {{cookiecutter.pkg_path}}.
    2. for each Java file, replace package name with {{cookiecutter.pkg_name}}
    3. for pom.xml, replace groupId, artifactId etc with {{cookiecutter.*}}
    4. for each yaml/yml file, repalce app name at end of line wih {{cookiecutter.project_name}}
    5. for each java,xml,yaml file, look for single line comments that begins with CC:, expose the content as template
    6. similarly, look for single line comments that begins with DELETE_IF:, write file names into to_delete.txt, which
       will be process with post_gen_hook.
    """

    source_svc_name, source_java_pkg = detect_java_pkg(base_path)
    template_path = copy_maven_project(base_path, output_path, source_java_pkg.replace(".", "/"))

    for root, dirs, files in os.walk(template_path, topdown=True):
        if ".mvn" in dirs:
            dirs.remove(".mvn")

        for src in files:
            src_path = root + "/" + src
            if src.endswith(".java"):
                replace_java_pkg(src_path, source_java_pkg)
            elif src == "pom.xml":
                process_pomxml(src_path)
            elif src.endswith(".yml") or src.endswith(".yaml") or src.endswith(".graphqls"):
                replace_slug_at_line_end(src_path, source_svc_name)

            process_comments(src_path)
            if len(to_delete_files) > 0:
                with open(template_path + "/to_delete.txt", "w") as f:
                    to_delete_files.sort()
                    f.write("\n".join(to_delete_files))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: migrate.py <maven project directory>")
        sys.exit(1)

    src_path = os.path.expanduser(sys.argv[1])
    if not os.path.exists(src_path):
        print(f"Usage: source path {src_path} does not exist")
        sys.exit(1)

    dest_path = sys.argv[2] if len(sys.argv) > 2 else "."
    migrate(src_path, ensure_dir_exists(dest_path))
