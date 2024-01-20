from setuptools import setup, find_packages

# TODO: Fill in the required fields in the following lines
setup(
    name='ReqFlow',
    version='1.0.0-alpha',
    packages=find_packages(),
    install_requires=[
        'httpx>=0.26.0'
        'jsonpath-ng>=1.6.1'
        'pydantic>=2.5.3'
    ],
    # Metadata
    author='Oleksii P.',
    description='A streamlined Python library for crafting HTTP requests and testing API',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',  # If your README is in Markdown
    url='https://github.com/olxxi/ReqFlow',  # Project home page
)
