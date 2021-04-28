import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="xtest", # Replace with your own username
    version="0.0.1",
    author="Cristian",
    author_email="xraid.rfid.test01@gmail.com",
    description="test rfid package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cristian-97/xtest",
    project_urls={
        "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    },
    install_requires=[            
        'requests',
    ],
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "rfid"},
    packages=setuptools.find_packages(where="rfid"),
    python_requires=">=3.6",
) 
