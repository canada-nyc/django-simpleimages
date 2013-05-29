from setuptools import setup

setup(
    name='django-simpleimages',
    version='0.1.7',
    author='Saul Shanabrook',
    author_email='s.shanabrook@gmail.com',
    packages=['simpleimages', 'simpleimages.test'],
    url='https://www.github.com/saulshanabrook/django-simpleimages',
    license='LICENSE.txt',
    description='Opinionated Django image transforms on models',
    long_description=open('README.rst').read(),
    install_requires=[
        "Django >= 1.5",
    ],
)
