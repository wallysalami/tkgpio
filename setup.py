import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tkgpio",
    version="0.1",
    author="Jan K. S.",
    author_email="developer@janks.software",
    description="A Python library to simulate Raspberry Pi GPIO devices in TkInter",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wallysalami/tkgpio",
    packages=setuptools.find_packages(),
    install_requires=[
        "gpiozero",
        "numpy",
        "Pillow",
        "scipy",
        "sounddevice",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
    include_package_data=True,
    package_data={
        "tkgpio": ["images/*"],
    }
)
