import os

from src import __version__ as version

readme = os.path.join(os.path.dirname(__file__), "README.md")
long_description = open(readme).read()

SETUP_ARGS = dict(
    name="<your project>",
    version=version,
    description="<your project description>",
    long_description=long_description,
    url="https://github.com/$(cat GITHUB_USER)/<your project>",
    author="<AUTHOR>",
    author_email="<EMAIL>",
    license="MIT",
    include_package_data=True,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.9",
    ],
    py_modules=[
        "src",
    ],
    install_requires=["sqlalchemy", "flask", "flask-cors"],
)

if __name__ == "__main__":
    from setuptools import find_packages, setup

    SETUP_ARGS["packages"] = find_packages()
    setup(**SETUP_ARGS)
