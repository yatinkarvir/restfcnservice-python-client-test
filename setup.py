from setuptools import setup, find_packages
from setuptools.command.build_py import build_py
import sys, platform


class _SetupVerifier(build_py):

    # MUST_BE_UPDATED_EACH_RELEASE (Search repo for this string)
    SUPPORTED_PYTHON_VERSIONS = {'3.9', '3.10', '3.11', '3.12'}

    PLATFORM_DICT = {
        'Windows': 'PATH',
        'Linux': 'LD_LIBRARY_PATH',
        'Darwin': 'DYLD_LIBRARY_PATH'
    }


    arch = ""
    python_ver = ""
    platform= ""
    path_env_var_name = ""
    verbose = False

    # ERROR MESSAGES

    unsupported_platform = "{platform:s} is not a supported platform."
    unsupported_python = "{python:s} is not supported. The supported Python versions are {supported:s}."

    def _print_if_verbose(self, msg):
        if self.verbose:
            print(msg)

    def set_platform_and_arch(self):
        """
        Sets the platform and architecture
        """
        self.platform = platform.system()
        if self.platform not in self.PLATFORM_DICT:
            raise RuntimeError(self.unsupported_platform.format(platform=self.platform))
        else:
            self.path_env_var_name = self.PLATFORM_DICT[self.platform]

        if self.platform == "Windows":
            self.arch = "win64"
        elif self.platform == "Linux":
            self.arch = "glnxa64"
        elif self.platform == "Darwin":
            if platform.mac_ver()[-1] == "arm64":
                self.arch = "maca64"
            else:
                raise RuntimeError(self.unsupported_platform.format(platform="maci64"))
        else:
            raise RuntimeError(self.unsupported_platform.format(platform=self.platform))


    def set_python_version(self):
        """
        Sets the Python version
        """
        ver = sys.version_info
        self.python_ver = f"{ver.major}.{ver.minor}"

        if self.python_ver not in self.SUPPORTED_PYTHON_VERSIONS:
            raise RuntimeError(self.unsupported_python.format(python=self.python_ver,
                                                              supported= str(self.SUPPORTED_PYTHON_VERSIONS)))


    def run(self):
        """
        Logic that will run prior to installation
        """
        self.set_platform_and_arch()
        self.set_python_version()

        build_py.run(self)


if __name__ == "__main__":
    with open("README.md", mode="r", encoding="utf-8") as readme:
        long_description = readme.read()

    setup(
        name="REST Function Service Python Client",
        version="26.1",
        author="MathWorks",
        license="LICENSE.txt located in this repository",
        url="https://github.com/yatinkavir/restfcnservice-python-client-test",
        long_description=long_description,
        long_description_content_type="text/markdown",
        package_dir={"": "src"},
        packages=find_packages(where="src"),
        cmdclass={'build_py': _SetupVerifier},
        package_data={'': ['_arch.txt']},
        zip_safe=False,
        project_urls={
            "Source": "https://github.com/yatinkavir/restfcnservice-python-client-test"
        },
        keywords=["MATLAB", "REST Function Service"],
        classifiers=[
            "Natural Language :: English",
            "Intended Audience :: Developers"
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.11",
            "Programming Language :: Python :: 3.12"
        ],
        # MUST_BE_UPDATED_EACH_RELEASE (Search repo for this string)
        python_requires=">=3.9, <3.13"
    )



