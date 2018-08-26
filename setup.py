import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "txttomp3",
    version = "1.0",
    author = "David Steele",
    author_email = "dsteele@gmail.com",
    description = ("Bulk conversion of text to MP3 speech, using the Google "
                   "Text-to-Speech service."),
    license = "GPL3",
    keywords = "text to speech audio mp3",
    url = "https://github.com/davesteele/txttomp3",
    packages=find_packages(),
    long_description=read('README.md'),
    entry_points={"console_scripts": ["txttomp3 = txttomp3.txttomp3:main"]},
    data_files=[("/var/cache/txttomp3", [])],
    python_requires=">=2.7,<3.0",
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    classifiers=[
    ],
)
