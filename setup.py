from setuptools import setup

setup(
    name='licytacje_api',
    version='0.1.0',    
    description='A package to interact with http://www.licytacje.komornik.pl',
    url='https://github.com/mianowski/licytacje_api',
    author='Grzegorz Mianowski',
    author_email='wiemioslo+licytacje_api@gmail.com',
    license='BSD 2-clause',
    packages=['licytacje_api'],
    install_requires=['beautifulsoup4>=4.4.0',
                      'babel>=2.7.0',
                      ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    console=['licytacje_api/main.py']
)