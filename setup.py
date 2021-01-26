from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='teamwork',  # Required
    version='0.1.0',  # Required
    description='A Python library for building a network graph of providers in care teams from EHR data',  # Optional
    long_description=long_description,  # Optional
    long_description_content_type='text/markdown',  # Optional (see note above)
    url='https://github.com/gtdelong/teamwork',  # Optional
    author='Grant DeLong',  # Optional
    author_email='ggoulae@gmail.com@example.com',  # Optional
    classifiers=[  # Optional
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Data Science',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
    ],
    keywords='team, collaboration, EHR',  # Optional
    package_dir={'': 'src'},  # Optional
    packages=find_packages(where='src'),  # Required
    python_requires='>=3.6, <4',
    install_requires=install_requires=[ # Optional
        'pandas',
        'numpy',
        'networkx'
    ], 
    project_urls={  # Optional
        'Source': 'https://github.com/gtdelong/teamwork/',
    },
)