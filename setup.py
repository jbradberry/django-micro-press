import setuptools


with open("README.rst") as f:
    long_description = f.read()


setuptools.setup(
    name='django-micro-press',
    version="0.2.0",
    author='Jeff Bradberry',
    author_email='jeff.bradberry@gmail.com',
    description='A pluggable app to embed a simple newpaper',
    long_description=long_description,
    long_description_content_type='test/x-rst',
    url='http://github.com/jbradberry/django-micro-press',
    packages=setuptools.find_packages(),
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python'
    ],
)
