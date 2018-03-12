from setuptools import find_packages, setup

setup(
    name='trains_python_tf',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
    ],
    test_suite='nose.collector',
    tests_require=[
        'nose'
    ],
)
