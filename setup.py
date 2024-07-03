from setuptools import setup, find_packages

setup(
    name='ReqFlow',
    version='1.0.9-alpha',
    packages=find_packages(),
    python_requires='>=3.8',
    install_requires=[
        'httpx>=0.26.0',
        'jsonpath-ng>=1.6.1',
        'pydantic>=2.5.3'
    ],
    # Metadata
    author='Oleksii P.',
    description='A streamlined Python library for crafting HTTP requests and testing API',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/olxxi/ReqFlow',
)
