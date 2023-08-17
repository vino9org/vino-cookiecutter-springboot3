from migrate import comment_regex


def test_regex_xml():
    re_comment, re_delif = comment_regex["xml"]

    line = "        <!-- CC: {% if cookiecutter.database_type == 'mongodb' -%} -->"
    match = re_comment.search(line)
    assert match
    assert match.group(1) == "        "
    assert "mongodb" in match.group(2)

    line = "        <!-- CC: {%- endif %} -->"
    match = re_comment.search(line)
    assert match
    assert match.group(1) == "        "
    assert "endif" in match.group(2)

    line = "        <!-- DELETE_IF: {% if cookiecutter.database_type != 'mongodb' %} -->"
    match = re_delif.search(line)
    assert match
    assert match.group(1) == "        "
    assert "mongodb" in match.group(2)

    line = "<!-- properites--->"
    match = re_comment.search(line)
    assert not match


def test_regex_java():
    re_comment, re_delif = comment_regex["java"]

    line = "        // CC: {% if cookiecutter.database_type == 'mongodb' -%} -->"
    match = re_comment.search(line)
    assert match
    assert match.group(1) == "        "
    assert "mongodb" in match.group(2)

    line = "        //   CC: {%- endif %} -->"
    match = re_comment.search(line)
    assert match
    assert match.group(1) == "        "
    assert "endif" in match.group(2)

    line = "// DELETE_IF: cookiecutter.cache_type != 'redis'"
    match = re_delif.search(line)
    assert match
    assert match.group(1) == ""
    assert "redis" in match.group(2)

    line = " // some CC random stuff not working"
    match = re_comment.search(line)
    assert not match


def test_regex_sql():
    re_comment, re_delif = comment_regex["sql"]

    line = "-- DELETE_IF: cookiecutter.database_type != 'postgresql' and cookiecutter.database_type != 'mysql'"
    match = re_delif.search(line)
    assert match
    assert match.group(1) == ""
    assert "postgres" in match.group(2)
