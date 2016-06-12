from setuptools import setup, find_packages

long_description = """
This Python utility and library is used to keep your secret value on Version Control Software. The secret value are encrypted with a public key so everyone can write them. However, the private key is required to decrypt those values. The private key should be stored only on the server running the app.
"""

setup(
    name='vcsecret',
    version='0.0.9',

    description='Keep your secrets in your VCS',
    long_description=long_description,
    url='https://github.com/isra17/vcsecret',
    author='isra17',
    author_email='isra017@gmail.com',
    license='LGPL3',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Security :: Cryptography',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities'
    ],

    keywords='secret config cryptography',

    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    entry_points={
        'console_scripts': [
            'vcsecret = vcsecret.main:main'
        ]
    },
    install_requires=['pycrypto']
)
