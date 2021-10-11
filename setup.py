from setuptools import setup, find_packages
import pathlib


here = pathlib.Path(__file__).parent.resolve()

long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='sample_test',  # Required
    version='0.0.1',  # Required
    description='A sample test for project',  # Optional
    long_description=long_description,  # Optional
    long_description_content_type='text/markdown',  # Optional (see note above)
    url='https://github.com/pypa/sampleproject',  # Optional
    author='JiaLe.tan',  # Optional
    author_email='jiale.gfi@outlook.com',  # Optional
    keywords='flask, test, sqlalchemy',  # Optional
    packages=find_packages(where='src'),  # Required
    install_requires=['sqlalchemy >= 1.0'],  # Optional
    python_requires='>=3.6, <4',
    project_urls={  # Optional
        'Bug Reports': 'https://github.com/pypa/sampleproject/issues',
        'Funding': 'https://donate.pypi.org',
        'Say Thanks!': 'http://saythanks.io/to/example',
        'Source': 'https://github.com/pypa/sampleproject/',
    },
)

