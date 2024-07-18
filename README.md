# Family Budget
The Soop API is built using Django and Django Rest Framework. It provides a comprehensive solution for maintaining and monitoring solar plants.

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

#### Launch the tests:

    $ docker compose -f local.yml run django pytest . -s

### API documentation with drf-spectacular

This project uses [drf-spectacular](https://drf-spectacular.readthedocs.io/en/latest/) to automatically
generate API documentation. All the available endpoints are listed at:
    
       http://localhost:8000/api/docs/


### GitHub Actions

This application uses GitHub Actions to automate the build and deployment process. 
Check the `.github-ci/workflows/ci.yml` file for more information.
