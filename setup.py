from setuptools import setup, find_namespace_packages

setup(
    name="depend_on_me",
    version="0.1.0",
    packages=find_namespace_packages(include='depend_on_me.*'),
    entry_points={
        'console_scripts': [
            'deployer = depend_on_me.deployer:main_func'
        ]
    },

    install_requires=[
        'PyYAML==5.1.2',
        'semantic-version==2.8.2'],

    author="Herbert Koelman",
    author_email="herbert.koelman@me.com",
    description="This is an Example Package",
    keywords="dependency handling example examples",
    url="https://github.com/HerbertKoelman/python_sample"
)
