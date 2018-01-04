from setuptools import setup

setup(
    name='example_app',
    packages=['example_app'],
    include_package_data=True,
    install_requires=[
        'flask',
        'requests'
    ],
)
