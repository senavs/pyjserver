import re
import setuptools

with open('README.md', encoding='utf-8') as file:
    long_description = file.read()

with open('pyjserver/__init__.py', encoding='utf-8') as file:
    version = re.findall(r'__version__[ ]=[ ][\'\"]((?:\d+[.]?){1,})[\'\"]', file.read())
    if version:
        version = version[0]
    else:
        version = '1.0.0'

requirements = [
    'flask==1.1.2',
]

setuptools.setup(
    name='pyjserver',
    version=version,
    license='MIT',
    install_requirements=requirements,
    description='Python implementation of Node JSON Server (Flask as backend)',
    author='Matheus Sena Vasconcelos',
    author_email='sena.matheus14@gmail.com',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/senavs/pyjserver',
    keywords=['python', 'node', 'nodejs', 'node.js',
              'json', 'server', 'pyjsonserver',
              'pyjserver', 'database', 'api', 'rest'],
    packages=['pyjserver', 'pyjserver.database', 'pyjserver.endpoint'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_required='>=3.6'
)
