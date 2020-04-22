#
# This file generates the sidebar/toctree for all RobotPy projects and should
# be copied to each project when it is updated
#

import os

def write_if_changed(fname, contents):

    try:
        with open(fname, "r") as fp:
            old_contents = fp.read()
    except:
        old_contents = ""

    if old_contents != contents:
        with open(fname, "w") as fp:
            fp.write(contents)


def generate_sidebar(conf, conf_api):

    # determine 'latest' or 'stable'
    # if not conf.do_gen:
    do_gen = os.environ.get("SIDEBAR", None) == "1" or conf["on_rtd"]
    version = conf["rtd_version"]

    lines = ["", ".. DO NOT MODIFY! THIS PAGE IS AUTOGENERATED!", ""]

    def toctree(name):
        lines.extend(
            [".. toctree::", "    :caption: %s" % name, "    :maxdepth: 2", ""]
        )

    def endl():
        lines.append("")

    def write(desc, link):
        if conf_api == "mlbench":
            args = desc, link
        elif not do_gen:
            return
        else:
            args = (
                desc,
                "https://mlbench.readthedocs.io/en/%s/%s.html" % (version, link),
            )

        lines.append("    %s <%s>" % args)

    def write_api(project, desc):
        if project != conf_api:
            if do_gen:
                args = desc, project, version
                lines.append(
                    "    %s API <https://mlbench.readthedocs.io/projects/%s/en/%s/api.html>"
                    % args
                )
        else:
            lines.append("    %s API <api>" % desc)

    def write_ref(project, desc):
        if project != conf_api:
            if do_gen:
                args = desc, project, version
                lines.append(
                    "    %s <https://mlbench.readthedocs.io/projects/%s/en/%s/readme.html>"
                    % args
                )
        else:
            lines.append("    %s <readme>" % desc)

    #
    # Specify the sidebar contents here
    #

    toctree("MLBench")
    write("Prerequisites", "prerequisites")
    write("Installation", "installation")
    write("Component Overview", "overview")
    write("Benchmarking Tasks", "benchmark-tasks")
    endl()

    toctree("Components")
    write_ref("mlbench_helm", "Helm Chart")
    write_ref("mlbench_dashboard", "Dashboard")
    write_ref("mlbench_benchmarks", "Benchmarks")
    write_api("mlbench_core", "Core")
    endl()

    toctree("Additional Info")
    write("Developer Guide", "devguide")
    write("Contributing", "contributing")
    write("Changelog", "changelog")
    endl()

    toctree("MLBench Developers")
    write("Authors", "authors")
    endl()

    write_if_changed("_sidebar.rst.inc", "\n".join(lines))
