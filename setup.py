from setuptools import find_packages, setup

setup(
    name='vocabulary_srv',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask', 'sqlalchemy', 'flask-security-too', 'pyjwt>=2', 'flask-cors', 'pyyaml',
        'flask_sqlalchemy', 'psycopg2-binary', 'dataclasses-json==0.5.4', "requests_oauthlib"
    ],
)
