from setuptools import setup


setup(
    name='django-simpleimages',
    version='0.2.8',
    author='Saul Shanabrook',
    author_email='s.shanabrook@gmail.com',
    packages=['simpleimages', ],
    url='https://www.github.com/saulshanabrook/django-simpleimages',
    license=open('LICENSE.txt').read(),
    description='Opinionated Django image transforms on models',
    long_description=open('README.rst').read(),
    install_requires=[
        "Django>=1.5,<1.6",
        "six"
    ],
    zip_safe=False  # so that django finds management commands
)
