from setuptools import setup


setup(
    name='prr',
    version='1.0',
    py_modules=['prr'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        prr=prr:cli
    ''',
)