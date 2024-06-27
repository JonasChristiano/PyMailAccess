from setuptools import setup, find_packages

setup(
    name='pymailaccess',
    version='0.1.0',
    author='Jonas Christiano',
    author_email='jonaschristianoti@gmail.com',
    description='A package for reading and sending emails using IMAPClient and SMTPLib.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/JonasChristiano/PyMailAccess',
    packages=find_packages(),
    install_requires=[
        'IMAPClient==3.0.1',
        'beautifulsoup4==4.12.3',
        'soupsieve==2.5'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)
