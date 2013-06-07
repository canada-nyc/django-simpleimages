from setuptools import setup, find_packages


setup(
    name='django-simpleimages',
    version='0.2.6',
    author='Saul Shanabrook',
    author_email='s.shanabrook@gmail.com',
    packages=find_packages(),
    url='https://www.github.com/saulshanabrook/django-simpleimages',
    license='LICENSE.txt',
    description='Opinionated Django image transforms on models',
    long_description=open('README.rst').read(),
    install_requires=[
        "Django >= 1.5",
    ],
    zip_safe=False  # so that django finds management commands
)
