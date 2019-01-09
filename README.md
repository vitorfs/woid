# Woid

[![Python Version](https://img.shields.io/badge/python-3.6-brightgreen.svg)](https://python.org)
[![Django Version](https://img.shields.io/badge/django-2.1-brightgreen.svg)](https://djangoproject.com)

**Table of Contents**

* [Running Locally](#running-locally)
* [Supported Services](#supported-services)
* [Crawlers](#crawlers)
  * [API Key Required: The New York Times](#the-new-york-times)
  * [API Key Required: Product Hunt](#product-hunt)
  * [Cron Jobs](#cron-jobs)
* [License](#license)

## Running Locally

First, clone the repository to your local machine:

```
git clone https://github.com/vitorfs/woid.git
```

Install the requirements:

```bash
pip install -r requirements/dev.txt
```

Apply the migrations:

```bash
python manage.py migrate
```

Load the initial data:

```bash
python manage.py loaddata services.json
```

Finally, run the development server:

```bash
python manage.py runserver
```

The site will be available at **127.0.0.1:8000**.

## Supported Services

Currently Woid crawl the following services to collect top stories: 

* Hacker News `hn`
* Reddit `reddit`
* GitHub `github`
* The New York Times `nytimes`
* Product Hunt `producthunt`


## Crawlers

You can run the crawlers manually to collect the top stories using the following command:

```bash
python manage.py crawl reddit
```

You can pass multiple services at once:

```bash
python manage.py crawl reddit hn nytimes
```

Valid values: `hn`, `reddit`, `github`, `nytimes`, `producthunt`.

### The New York Times

To crawl The New York Times you will need an API key.

You can register one application at [developer.nytimes.com](https://developer.nytimes.com).

### Product Hunt

Product Hunt require an API key to consume their API. 

You can register one application at [api.producthunt.com/v1/docs](https://api.producthunt.com/v1/docs)

### Cron Jobs

You can set up cron jobs to execute the crawlers periodically. Here is what my crontab looks like:

```
*/5 * * * * /home/woid/venv/bin/python /home/woid/woid/manage.py crawl reddit hn producthunt >> /home/woid/logs/cron.log 2>&1
*/30 * * * * /home/woid/venv/bin/python /home/woid/woid/manage.py crawl nytimes github >> /home/woid/logs/cron.log 2>&1
```

## License

The source code is released under the [Apache 2.0 license](https://github.com/vitorfs/woid/blob/master/LICENSE).
