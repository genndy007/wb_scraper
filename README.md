# Wildberries Goods Scraper/Monitor

This software lets you to set regular scraping of goods at Wildberries Marketplace. 
You can add articuls of particular goods you are interested in, and then get information 
about cost changes in certain period of time.


## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Tests](#tests)
- [Support](#support)
- [Contributing](#contributing)

## Installation

Download project to your computer, change to project directory, then:

#### Build with hands
```sh
# Run with Python3, PostgreSQL and Celery[RabbitMQ]
cp .env.example .env  # fill env file with values
pip install poetry
poetry install   # --no-dev flag for no testing libs

# terminal 1
sudo rabbitmq-server   # run queue backend
# terminal 2
createdb wb_app -O postgres -U postgres   # create postgres database
# terminal 3
poetry run python ./src/manage.py runserver 0.0.0.0:8000   # django backend
# terminal 4
cd ./src
poetry run celery -A main worker -B -l INFO   # celery tasks worker 
```

#### Compose
```sh
docker-compose build
docker-compose up
```

## Usage

I hope I would add Swagger interactive documentation

#### User authentication
|Request               | Definition                |
|----------------------|---------------------------|
|POST /users/register/ | Register a new user       |
|POST /users/login/    | Login into account        |
|GET /users/me/        | Check yourself logged in  |
|POST /users/logout/   | Log out                   | 


#### Cards CRUD
|Request                                                         |Definition           |
|----------------------------------------------------------------|---------------------|
|POST /cards/                                                    | Add new card        |
|GET /cards/                                                     | Get all your cards  |
|DELETE /cards/                                                  | Delete all cards    |
|DELETE /cards/1/                                                | Delete one card     |
|GET /cards/update/                                              | Update stats now    |
|GET /cards/1/stats?start=2022-01-01&end=2023-01-01&interval=1   | Retrieve statistics |


## Tests
To run all tests
```sh
# testing libs must be installed 
poetry install
poetry shell
./test.sh
```


## Support

Check my [GitHub account page](https://github.com/genndy007/) for contacts.
Please [open an issue](https://github.com/genndy007/wb_scraper/issues/new) for support.

## Contributing

Please contribute using [GitHub Flow](https://guides.github.com/introduction/flow/). 
Create a branch, add commits, and [open a pull request](https://github.com/genndy007/wb_scraper/compare/).
