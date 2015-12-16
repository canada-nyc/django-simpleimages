from setuptools import setup


setup(
    name='django-simpleimages',
    version='1.3.1',
    author='Saul Shanabrook',
    author_email='s.shanabrook@gmail.com',
    packages=[
        'simpleimages',
        'simpleimages.management',
        'simpleimages.management.commands',
    ],
    url='https://www.github.com/saulshanabrook/django-simpleimages',
    license=open('LICENSE.txt').read(),
    description='Opinionated Django image transforms on models',
    long_description=open('README.rst').read(),
    install_requires=[
        "Django>=1.5,<1.10",
        "six",
        "Pillow",
        'clint',
    ],
    zip_safe=False,  # so that django finds management commands,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Framework :: Django',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries',
    ],
)
