"""Setup script for vecto package."""

import setup_boilerplate


class Package(setup_boilerplate.Package):

    """Package metadata."""

    name = 'protonn'
    description = 'neural prototyping framework'
    url = "https://protonn-ai.github.io/"
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Scientific/Engineering']
    keywords = ['machine learning', 'prototyping', 'neural network']


if __name__ == '__main__':
    Package.setup()
