from setuptools import setup

setup(
    name='mkdocs-autoreflinks-plugin',
    version='1.0.0',
    author='Paul Ouellette',
    description='An MkDocs plugin that auto-links heading references',
    url='https://github.com/pauloue/mkdocs-autoreflinks-plugin',
    packages=['autoreflinks'],
    install_requires=['mkdocs', 'bs4'],

    entry_points={
        'mkdocs.plugins': [
            'autoreflinks = autoreflinks.plugin:AutoRefLinks',
        ]
    },
)
