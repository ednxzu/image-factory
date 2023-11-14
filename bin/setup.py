from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="factory",
    version="1.0.0",
    packages=find_packages(),
    package_data={'factory': ['functions/*']},
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'factory=factory.__main__:main',
        ],
    },
)
