from setuptools import setup, find_packages

install_requires = [
]

setup(
    name='pierogi',
    version='0.1.0',
    python_requires='>=3.5',
    packages=find_packages(),
    include_package_data=True,
    author='Manu NALEPA',
    author_email='nalepae@gmail.com',
    description='Visualiwze and tweak your Machine Learning model.',
    long_description='See https://github.com/nalepae/pierogi/tree/v0.1.0 for complete user guide.',
    url='https://github.com/nalepae/pierogi',
    install_requires=install_requires,
    license='BSD',
)
