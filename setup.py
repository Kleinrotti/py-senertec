import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="py-senertec",
    version="0.3.0",
    author="Kleinrotti",
    author_email="",
    package_dir={"": "src"},
    packages=setuptools.find_packages("src"),
    description="Senertec energy system gen2 interface.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Kleinrotti/py-senertec",
    project_urls={
        "Bug Tracker": "https://github.com/Kleinrotti/py-senertec/issues",
    },
    python_requires='>=3.6',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
         "websocket-client>=1.2.3",
         "requests>=2.27",
         "beautifulsoup4>=4.11"
    ]
)