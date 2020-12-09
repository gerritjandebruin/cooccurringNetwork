import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cooccurringNetwork",
    version="0.0.1",
    author="Gerrit-Jan de Bruin",
    author_email="gerritjan.debruin@gmail.com",
    description="Module to create cooccuring networks from event data.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://github.com/gerritjandebruin/cooccurringNetwork",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)