from io import open
from setuptools import setup

with open('README.md') as read_me:
    long_description = read_me.read()

setup(
    name='EelS',
    version='0.1.0',
    author='mhbalthasar',
    author_email='scskarsper@163.com',
    url='https://github.com/mhbalthasar/EelS',
    packages=['eels'],
    install_requires=['eel'],
    extras_require={
        "jinja2": ['jinja2>=2.10']
    },
    python_requires='>=3.6',
    description='Eel is a little HTML GUI applications, with easy Python/JS interop.And Eels is a scaffold of it,it include the electron dist and embbed it into Eel.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=['gui', 'html', 'javascript', 'electron'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Natural Language :: English',
        'Operating System :: MacOS',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows :: Windows 10',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'License :: OSI Approved :: GPL3 License',
    ],
)
