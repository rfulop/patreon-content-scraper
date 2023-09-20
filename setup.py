from setuptools import setup, find_packages

setup(
    name='patreon-content-scraper',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'requests',
        'beautifulsoup4',
        'python-dotenv',
        ],
    entry_points={
        'console_scripts': [
            'patreon-content-scraper=patreon_content_scraper.main:main',
        ],
    },

    author='rfulop',
    license='MIT',
    description='A simple tool to scrape content from Patreon.',
    url='https://github.com/rfulop/patreon-content-scraper',
    keywords='patreon scraper content',
)
