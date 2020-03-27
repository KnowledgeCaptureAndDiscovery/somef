from setuptools import setup

setup(name='sm2kg',
        version='0.2',
        description='test desc',
        packages=['sm2kg'],
        install_requires=[
            'numpy',
            'pandas',
            'sklearn',
            'nltk',
            'matplotlib',
            'bs4',
            'requests',
            'markdown',
        ],
        include_package_data=True,
        zip_safe=False)
