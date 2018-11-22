from setuptools import setup
import nested_diff


with open('README.md') as f:
    long_description = f.read()

setup(
    name='nested_diff',
    version=nested_diff.__version__,
    description='Recursive diff for nested structures',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='diff nested-diff recursive-diff nested-data data-structures',
    url='https://github.com/mr-mixas/Nested-Diff.py',
    author='Michael Samoglyadov',
    author_email='mixas.sr@gmail.com',
    license='Apache License 2.0',
    packages=['nested_diff'],
    test_suite='tests',
    setup_requires=["pytest-runner"],
    tests_require=['pytest'],
    include_package_data=True,
    zip_safe=False
)
