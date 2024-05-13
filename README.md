# Emeraldhouse

Job application tracker for onsiteiq take home

## Local development

At a high level, there are 3 tools used to facilitate building + running the application.

- Docker is responsible for containerizing the applications and reducing cross platform issues
- Docker Compose is used to orchestrate the containers and allow for different combinations to be started
- GNU Make was used to expose several common application actions with the goal of improving developer experience

### Prerequisites

You must verify a few things prior to attempting to run this application.

- x86 architecture
  - Currently, this project requires x86 architecture to run. The instructions on how to verify this depend upon the specifics of your system and is outside the scope of this README.
- Docker #TODO: get min version
  - You may verify your Docker version by running `Docker version`
  - If you need to update or install Docker, instructions are available at https://docs.docker.com/engine/install/
- Docker Compose
  - You may verify your Docker Compose version by running `docker compose version`
  - Installation instructions are available at https://docs.docker.com/compose/install/
- GNU Make
  - You may verify installation by running `make --version`
  - Installation instructions are somewhat dependent upon operating system. Most linux distros will include it out of the box while macOS users should be able to install with Homebrew. Anyone using windows will have to report back on whether there are difficulties. In theory, windows users should be able to use these binaries https://gnuwin32.sourceforge.net/packages/make.htm

### Provisioning environment

There are a couple extra commands to run the first time the application begins. We need to:

- Pull & Build the app containers
- Run Django migrations
- Seed the database
- Start the server

All of these steps may be accomplished with a single command:

```
make pull app_build migrate seed run
```

### Starting server for development

After you have run the provisioning command once, you may start the server for development with:

```
make run
```

### Provided commands

Several commands are exposed through the Makefile:

- `make run`
  - The basic command which will start the containerized Django server as well as the postgres db
- `make migrate`
  - Will run Django migrations using `python manage.py migrate` under the hood. The db includes a volume, so this command will be persistent across containers.
- `make migrations`
  - Will run the Django migration generation script. It examines model files for changes and is equivalent to running `python manage.py makemigrations`
- `make pull`
  - Re-pulls docker images from the compose file
- `make app_build`
  - Rebuilds the Django app's docker container
- `make shell`
  - Drops the user into a Django shell using `python manage.py shell`
- `make seed`
  - Runs a database seed script to facilitate interacting with the API
- `make test`
  - Runs the test suite
