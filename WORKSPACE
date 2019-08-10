workspace(name = "unfollowuserbot")

load("@bazel_tools//tools/build_defs/repo:git.bzl", "git_repository")

git_repository(
    name = "rules_python",
    remote = "https://github.com/bazelbuild/rules_python.git",
    commit = "6c5f479420b0a086e3bc7a6d7c818196d0c89ad8",
)

load("@rules_python//python:pip.bzl", "pip_repositories", "pip_import")

pip_repositories()

pip_import(
    name = "third_party_deps",
    requirements = "//:requirements.txt",
)

load("@rules_python//python:pip.bzl", "pip_import")

pip_import(
   name = "my_deps",
   requirements = "//:requirements.txt",
)

load("@my_deps//:requirements.bzl", "pip_install")
pip_install()