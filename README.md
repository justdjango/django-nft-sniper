djsniper
========

Django Self-Hosted NFT Rarity Sniper

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)

[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

### Notes

How to calculate rarity: https://raritytools.medium.com/ranking-rarity-understanding-rarity-calculation-methods-86ceaeb9b98c
ERC721 Token standard: https://ethereum.org/en/developers/docs/standards/tokens/erc-721/
Look for token on etherscan -> contract -> read contract -> tokenURI method
Get the ABI from the contract on etherscan ->  contract -> code -> Contract ABI
Interacting with contracts via web3.py -> https://web3py.readthedocs.io/en/latest/examples.html#interacting-with-existing-contracts
How to find your NFT on IPFS -> https://medium.com/coinmonks/how-to-find-your-nft-on-ipfs-e51bc5e7c8a1#:~:text=Find%20your%20NFT's%20Metadata&text=Look%20for%20a%20function%20called,NFT%20(see%20figure%201).
License

:   MIT

Settings
--------

Moved to
[settings](http://cookiecutter-django.readthedocs.io/en/latest/settings.html).

Basic Commands
--------------

### Setting Up Your Users

-   To create a **normal user account**, just go to Sign Up and fill out
    the form. Once you submit it, you\'ll see a \"Verify Your E-mail
    Address\" page. Go to your console to see a simulated email
    verification message. Copy the link into your browser. Now the
    user\'s email should be verified and ready to go.

-   To create an **superuser account**, use this command:

        $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and
your superuser logged in on Firefox (or similar), so that you can see
how the site behaves for both kinds of users.

### Type checks

Running type checks with mypy:

    $ mypy djsniper

### Test coverage

To run the tests, check your test coverage, and generate an HTML
coverage report:

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

#### Running tests with py.test

    $ pytest

### Live reloading and Sass CSS compilation

Moved to [Live reloading and SASS
compilation](http://cookiecutter-django.readthedocs.io/en/latest/live-reloading-and-sass-compilation.html).

### Celery

This app comes with Celery.

To run a celery worker:

``` {.bash}
cd djsniper
celery -A config.celery_app worker -l info
```

Please note: For Celery\'s import magic to work, it is important *where*
the celery commands are run. If you are in the same folder with
*manage.py*, you should be right.

### Sentry

Sentry is an error logging aggregator service. You can sign up for a
free account at <https://sentry.io/signup/?code=cookiecutter> or
download and host it yourself. The system is setup with reasonable
defaults, including 404 logging and integration with the WSGI
application.

You must set the DSN url in production.

Deployment
----------

The following details how to deploy this application.

### Docker

See detailed [cookiecutter-django Docker
documentation](http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html).
