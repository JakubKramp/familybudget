# Family Budget

Recruitment task for Kelton Europe

## Prerequisites

Before you begin, ensure you have met the following requirements:

- You have installed the latest version of Docker and Docker Compose.


## Local development

Follow the steps below to get started with local development.


#### Build the images:

    $ docker compose -f local.yml build

#### Run the containers:

    $ docker compose -f local.yml up

#### Create superuser:

    $ docker compose -f local.yml run django python manage.py createsuperuser

#### Load initial data [optional]:

    $ docker compose -f local.yml run django python manage.py loaddata fixtures/fixtures.json



#### Launch the tests:

    $ docker compose -f local.yml run django pytest . -s

### API documentation with drf-spectacular

This project uses [drf-spectacular](https://drf-spectacular.readthedocs.io/en/latest/) to automatically
generate API documentation. All the available endpoints are listed at:
    
       http://localhost:8000/api/docs/


### GitHub Actions

This application uses GitHub Actions to automate the build and deployment process. 
Check the `.github-ci/workflows/ci.yml` file for more information.
