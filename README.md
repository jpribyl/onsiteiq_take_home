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

### Provisioning environment (quickstart)

There are a couple extra commands to run the first time the application begins. We need to:

- Pull & Build the app containers
- Run Django migrations
<!--- Seed the database # TODO - at present there is no database seeding-->
- Start the server

All of these steps may be accomplished with a single command:

```
make pull app_build migrate run
```

### Running test suite

The test suite provides a coverage report and may be run using:

```
make test
```

Additional options may be passed using the `pytest_options` variable:

```
make test pytest_options="-k test_applicant_api"
```

### Starting server for development

After you have run the provisioning command once, you may start the server for development with:

```
make run
```

### Creating a user capable of authentication

Once the app has been built, you may create a new user using the add_or_update_employee command. In order for this user to be able to actually take any actions in the API they must be given group or object level permissions. If you wish to give full access to a new user, this may be accomplished by including all permission groups. For example, you may wish to run something like this:

```
make add_or_update_employee first_name=first last_name=last email=first@last.com password=password security_groups="add_all_applicant view_all_applicant change_all_applicant view_all_applicantnote add_all_applicantnote"

```

### Permission overview

The program makes use of groups as well as object based permission rules. Groups are used to allow a user to have full access of a given model + action combination. For example, a group of "add_all_applicantnote" will allow a user to add ANY applicant note regardless of what applicant / job posting it may be related to.

There are three levels of permissions:

1.  APPLICANT

    - This will allow the user to take an action for a particular applicant. For example, that user may be able to view all notes associated with that applicant or transition that applicant from one state to another.

2.  JOB POSTING

    - This allows the user to take an action for all applicants in a particular job posting. For example, the user may be able to view all notes associated with any applicant of that particular job posting.

3.  ALL

    - As mentioned above, this uses groups and allows access to manage all rows of a given table / action combination.

The goal here is to provide sane & decently granular permissions without providing too many that won't have a use case. For example, at present it is NOT possible to limit a user to seeing only SOME NOTES for a given APPLICANT -- however, it is possible to limit a user to seeing only that applicant's notes.

### Permission utility functions

Alternatively, user permissions may be handled through utility functions in the django shell. For example, you may run:

```
make shell
```

to be dropped into a django shell that is connected to the database. Once there, you may run any function you desire. For example, in order to provide full access to all applicant groups you may run:

```
from emeraldhouse.permissions import utils as permission_utils
from django.contrib.auth import models as django_contrib_auth_models
user = django_contrib_auth_models.User.objects.get(email=<REPLACE WITH YOUR USER'S EMAIL>)
permission_utils.allow_user_full_applicant_access(user)
```

You could run something like this if you wanted to allow a user to manage applicants related to a single job posting:

```
from emeraldhouse.permissions import utils as permission_utils
permission_utils.create_user_job_posting_applicant_permission(
    user_id=<REPLACE WITH YOUR USER ID>,
    job_posting_id=<REPLACE WITH YOUR JOB POSTING ID>,
    permission_codename=<REPLACE WITH RELEVANT PERMISSION CODENAME -- IE (add|change|view)_applicant>
)
```

Or, if you wanted to allow a user to manage all applicant notes related to a single job posting:

```
from emeraldhouse.permissions import utils as permission_utils
permission_utils.create_user_job_posting_applicant_note_permission(
    user_id=<REPLACE WITH YOUR USER ID>,
    job_posting_id=<REPLACE WITH YOUR JOB POSTING ID>,
    permission_codename=<REPLACE WITH RELEVANT PERMISSION CODENAME -- IE (add|view)_applicantnote>
)
```

If you wanted to give a user access to a single applicant, that would be done with something like this:

```
from emeraldhouse.permissions import utils as permission_utils
permission_utils.create_user_applicant_permission(
    user_id=<REPLACE WITH YOUR USER ID>,
    job_posting_id=<REPLACE WITH YOUR JOB POSTING ID>,
    permission_codename=<REPLACE WITH RELEVANT PERMISSION CODENAME -- IE (add|change|view)_applicant>
)
```

Or you wanted to give a user access to a single applicant's notes, that would be done with something like this:

```
from emeraldhouse.permissions import utils as permission_utils
permission_utils.create_user_applicant_note_permission(
    user_id=<REPLACE WITH YOUR USER ID>,
    job_posting_id=<REPLACE WITH YOUR JOB POSTING ID>,
    permission_codename=<REPLACE WITH RELEVANT PERMISSION CODENAME -- IE (add|view)_applicantnote>
)
```

Currently, there are no utility functions to remove permissions, so you would have to remove them directly through the django ORM or sql. Object permissions exist in the `UserObjectPermission` model while group permissions exist on the django contrib auth `Group` model.

### Authenticating to the API

API calls use JWT tokens for authentication. In order to make an authenticated request to the API there are two steps.

#### Token generation

First, the user must generate a token. This may be done through the django shell or an API endpoint. In order to do it through the endpoint you may do something like this:

```
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"username": <REPLACE WITH YOUR USENAME>, "password": <REPLACE WITH YOUR PASSWORD>}' \
  http://localhost:8654/api/token/
```

The response will be a JSON blob with the access token under the key "access". If you prefer to do it through the django shell you may do it like so:

```
from emeraldhouse.permissions import utils as permission_utils
permission_utils.get_tokens_for_user(<REPLACE WITH YOUR USER OBJECT>)
```

As before, the access token will be returned under the key "access".

#### Using the token to submit authenticated requests

Now that you have a token, you may include it under the "Authorization" header in your http request like so:

```
curl -X GET \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJh....yEhw" \
  http://localhost:8654/applicants/
```

By default, token lifespan will be set to 30 minutes. If you would like to change this, it may be done with the following setting in `emeraldhouse/config/settings.py`:

```
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": datetime.timedelta(minutes=30),
}
```

### API Documentation

The project uses `drf-spectacular` in order to generate and serve swagger docs. In order to generate the docs you may navigate to:

```
http://localhost:8654/api/schema/swagger-ui/
```

while the app is running. Hopefully these docs are fairly self-explanatory. They may be used to interact with the API. First you must authenticate by hitting the token endpoint and pasting the "access" value into the "authorize" pop-up value box. After that, you will be able to take any actions for which the authenticated user has permission to take.

### Debugging the program

The backend docker container exposes port 6900 for debugging. You may attach whatever debugger you choose to this port. I have included `pudb` which will allow you to set a trace for remote debugging like this:

```
from pudb.remote import set_trace
set_trace(term_size=(160, 40), host='0.0.0.0', port=6900)
```

Depeding upon the size of your screen, you may want to customize the terminal size. Once you have triggered the debugger, you may attach to it using telnet:

```
telnet localhost 6900
```

Any other remote debugger should attach in a similar fashion.

### Changing ORM models

The project relies upon Django's migration management. It exposes a command which will examine model files and create migration files from them:

```
make migrations
```

### Provided commands

Several commands are exposed through the Makefile:

- `make add_or_update_employee`
  - Will add a new employee capable of authentication to the database. If there is an existing user with that email, then it will instead overwrite the groups with those provided
- `make add_packages`
  - Installs packages and rebuilds docker containers. Usage requires an argument of 'packages': `make add_packages packages="<some python package> <some other python package>"`
- `make app_build`
  - Builds the app docker-compose profile
- `make bash`
  - Drops the user into a bash session on the docker container
- `make help` (Or simply `make`)
  - print help message
- `make migrate`
  - Runs Django migrations using `python manage.py migrate`
- `make migrations`
  - Analyzes Django model files for changes using `python manage.py makemigrations`
- `make pip_install`
  - Installs pip packages. Usage requires an argument of 'packages': `make pip_install packages="<some python package> <some other python package>"`
- `make pull`
  - Pulls docker containers
- `make run`
  - Runs the dockerized application for development
- `make shell_build`
  - Builds the Django shell docker-compose profile
- `make shell`
  - Drops the user into a Django shell using `python manage.py shell`
- `make test`
  - Runs the test suite using pytest

## Curl commands to satisfy the project's requirements

### Create Applicants?

```
curl -X 'POST' \
  'http://localhost:8654/applicants/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: <REPLACE WITH YOUR TOKEN>' \
  -d '{
  "user": {
    "first_name": "first",
    "last_name": "last",
    "email": "first@last.com"
  },
  "job_posting": {
    "title": "engineer"
  }
}'
```

### Create Applicant Notes?

```
curl -X 'POST' \
  'http://localhost:8654/applicants/<REPLACE WITH YOUR APPLICANT ID>/add_note/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: <REPLACE WITH YOUR TOKEN>' \
  -d '{
  "text": "string",
  "applicant_id": 0
}'
```

### Retrieve Applicant Notes?

Note- this was not explicitly asked for, however it is possible for a user to have view access to an applicant without having view access to their notes. So, I have not attached them to the applicant response. A future improvement would be to attach them there when / if they are viewable.

```
curl -X 'GET' \
  'http://localhost:8654/applicants/<REPLACE WITH YOUR APPLICANT ID>/view_notes/' \
  -H 'Authorization: <REPLACE WITH YOUR TOKEN>' \
  -H 'accept: application/json'
```

### Approve or Reject a candidate?

```

# Approve a candidate
curl -X 'POST' \
 'http://localhost:8654/applicants/<REPLACE WITH YOUR APPLICANT ID>/transition_applicant/' \
 -H 'accept: application/json' \
 -H 'Content-Type: application/json' \
 -H 'Authorization: <REPLACE WITH YOUR TOKEN>' \
 -d '{
"state": "APPROVED"
}'

# Reject a candidate
curl -X 'POST' \
 'http://localhost:8654/applicants/<REPLACE WITH YOUR APPLICANT ID>/transition_applicant/' \
 -H 'accept: application/json' \
 -H 'Content-Type: application/json' \
 -H 'Authorization: <REPLACE WITH YOUR TOKEN>' \
 -d '{
"state": "REJECTED"
}'

```

### Respect permissions?

Left as an exercise to the reader.
