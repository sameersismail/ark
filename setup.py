from setuptools import setup, find_packages

requirements = [
    "pygments",
    "pyxdg",
    # "mistune", # Packaged in-source
]

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="ark",
    version="0.1.0",
    packages=find_packages(),
    url="github.com",
    install_requires=requirements,
    extras_require={
        'dev': [
            'pytest',
            'pytest-cov',
        ]
    },
    install_package_data=True,
    author="First Name",
    author_email="name@domain",
    license="",
    long_description=long_description,
    entry_points={
        'console_scripts': [
            'ark=ark.cli.main:main',
            'arkp=ark.cli.pic:main',
        ],
    },
)
