import setuptools

import nested_diff


with open('README.md') as f:
    long_description = f.read()

setuptools.setup(
    name='nested_diff',
    version=nested_diff.__version__,
    description='Recursive diff for nested structures',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='diff nested-diff recursive-diff nested-data data-structures',
    url='https://github.com/mr-mixas/Nested-Diff.py',
    author='Michael Samoglyadov',
    author_email='mixas.sr@gmail.com',
    license='Apache License 2.0',
    packages=['nested_diff'],
    entry_points={
        'console_scripts': [
            'nested_diff=nested_diff.diff_tool:cli',
            'nested_patch=nested_diff.patch_tool:cli',
        ],
    },
    extras_require={
        'cli': [
            'pyyaml',
            'toml',
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
