from setuptools import setup

with open("README.rst", "rb") as f:
    long_descr = f.read().decode('utf-8')

setup(
    name = "getsong",
    packages = ["getsong"],
    install_requires = ["beautifulsoup4", "youtube-dl"],
    entry_points = {
        "console_scripts": ['getsong = getsong.getsong:main']
        },
    version = "1.1.5",
    description = "A Python program which uses BeautifulSoup and Youtube-dl to download a song from youtube",
    long_description = long_descr,
    author = "Steven Smith",
    author_email = "stevensmith.ome@gmail.com",
    license = "MIT",
    url = "https://blha303.github.io/getsong/",
    classifiers = [
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: System Administrators",
        "Topic :: Multimedia :: Sound/Audio"
        ]
    )
