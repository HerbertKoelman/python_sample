from setuptools import setup, find_packages

def requirements():
    requirments = []
    with open('requirements.txt', 'r') as file:
        requirements = file.readlines()

    return requirements

setup(
    name="artifacts",
    version="0.1",

    packages=find_packages(include=['artifacts'],exclude=['tests','venv']),

    entry_points={
        'console_scripts': [
            'artifact-deploy   = artifacts.deploy_artifacts_app:main',
            'artifact-copy     = artifacts.copy_artifacts_app:main'
        ]
    },

    install_requires=['PyYAML==5.1.2', 'semantic-version==2.8.2'],

    author="Herbert Koelman",
    author_email="herbert.koelman@me.com",
    description="Handles artifacts",
    keywords="handling artifacts",
    url="https://github.com/HerbertKoelman/python_sample"
)
