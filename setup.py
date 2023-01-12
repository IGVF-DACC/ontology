from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

setup(
    name='ontology',
    version='0.1.0',
    description='package for update ontology',
    long_description=readme,
    url = 'https://github.com/IGVF-DACC/ontology',
    maintainer='Mingjie Li',
    maintainer_email='mingjiel@stanford.edu',
    package_dir = {"ontology": "ontology"},
    packages=find_packages(exclude=('tests', 'docs')),

    entry_points = {
        "console_scripts": [
            "generate_ontology = ontology.generate_ontology:main"
        ]
    },

    install_requires = [
        "rdflib==6.2.0",
        "requests==2.27.1"
    ],
)