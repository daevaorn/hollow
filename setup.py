from distutils.core import setup


setup(
    name='hollow',
    version='0.1',
    description='Django ORM mocking library',

    author='Alex Koshelev',
    author_email='daevaorn@gmail.com',

    url='https://github.com/daevaorn/hollow',

    packages=[
        'hollow',
        'hollow.tests',
    ],
)
