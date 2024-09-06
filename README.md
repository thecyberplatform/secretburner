# Secret Burner

Secure, single-use secrets that vanish after viewing.

# Technical Details

Secret Burner has been built on a core stack of open source technologies:
```
- API : Django (https://djangoproject.com)
- UI  : Quasar (https://quasar.dev)
- DB  : PostgreSQL (https://www.postgresql.org)
```

## Directory Structure

The following describes the directory structure of the project.

```
app/
    ui/
        src/
            assets/ - Not used in this project.
            boot/ - Contains library injection for Internationalisation
            components/ - Globally re-usable components
            composables/ - Business logic for the application
            css/ - Custom styling
            i18n/* - Language files for the app
            layouts/ - Contains the global layout component.
            pages/ - Contains page views for the functionality of the app.
            router/ - Routing configuration
            types/ - Typescript typing for the app - soon to be deprecated in favour of functional containment of types.
    api/
        core/
            base/ - A base app for helper functions, generic middleware and other reusable tools.
        secret/
            api/ - The API logic including routing, serialisation and views.
            migrations/ - Standard Django migration files
            templates/ - Templates for emailing
        config/ - This is where the settings, requirements and ROOT_URLS entrypoint live.
deploy/
    aws/ - Terraform files for deploying into a default VPC on ECS with S3 for static UI website.
    docker/ - Files necessary to build the project locally on docker using Docker Compose.
    render/ - Deployment files for render.com
        
```

## Principles

The project is structured such that functionality is largely contained. 

# Makefile

This project has a customised Makefile to provide shortcuts to otherwise long commands. 

To get acquainted with all the available commands, simply run `make help`.

# Local development

Local builds of this application have only been tested on MacOS 14+.

Feel free to test on other operating systems and submit a pull request to add functionality where it
is lacking.

## Preparing for local build

In each "app", you will need to rename the .example.env file to .env

Change any settings that you want, or leave them blank if they are marked as optional.

All environment variables are described. You should never need to modify configuration/setting files inside 
the apps - all default user controllable features can be managed from .env files.

### Install docker

You will need to install docker. Google search this if you don't know how to do it.

## Running locally

To run secret burner, navigate back to the root of this project, and using the terminal run:

```bash
make up
```
This will build all the services needed to run the whole application. Just like magic.

Once it's done, you should be able to navigate to http://localhost and start creating secrets!

# Production deployment

TBC - This is still work in progress.