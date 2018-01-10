from setuptools import setup


setup(
    name='nested_diff',
    version='0.1',
    description='Recursive diff for nested structures',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
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
