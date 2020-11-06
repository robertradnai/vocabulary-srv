from setuptools import find_packages, setup

setup(
    name='vocabulary_srv',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask', 'sqlalchemy', 'flask-security-too', 'pyjwt', 'flask-cors', 'pytest', 'pyyaml'
    ],
)
