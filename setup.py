from setuptools import version, setup, find_packages
import artifacts

setup(
    name="artifacts",
    version=artifacts.__version__.__str__(),

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
    description="""
    basic artifact handler.
    
    if you are sane, setup something like conan (https://conan.io).
    
    the system relies on archive files and directories. Artifacts are anything found in a tape archive ist's name follows 
    this rule '<name>[-<os>]-<semver>[-snapshot]-<target arch>.tar.gz'. Degist files are expected to use this naming 
    rule '<name>[-<os>]-<semver>[-snapshot]-<target arch>.tar.gz.md5'.
    
    The modules comes with two programs, one that coipies your artifacts into a directory. And another that searches your 
    artifact directories and extracts whatever wad archived.
    
    what this module does and you, who are using mv, cp and tar commands, is: we do check file integrity (MD5) before copying 
    or archive extraction. Plus we run on both windows and Unix :-) 
    """,
    keywords="handling artifacts",
    url="https://github.com/HerbertKoelman/python_sample",
    licence='GPLv3+',

    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Environment :: Console'
    ]
)
