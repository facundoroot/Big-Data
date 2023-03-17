-- after docker-compose up
docker exec -it [container_name] bash
psql -U [user] -W [database]

-- if i want to delete volumes also
docker-compose down --volume

-- if airflow can't locate revision identified by
means that the alembic version is failing for some reason, probably changed something on the yaml
docker-compose down -v

-------------------------------------------------------------


-- Docker ports
Usually when we create a service on docker compose for example the postgres_database we use
local_port_mapping:inside_container_port, so you would try to connect to the local_port_mapping from
localhost:local_port_mapping and when you connect to that port it will forward/map your request to
inside_container_port inside container.
On the other hand, docker compose creates a default network when spinning the docker compose so the
services can connect between each other,so here on our docker compose, we are creating
AIRFLOW_CONN_DW_ANALYTICS with host as the name of the container name from postgres_database (postgres_database) so instead of connecting to local_port_mapping we can connect directly to the postgres database inside the container: postgres_database:inside_container_port.

-------------------------------------------------------------


--mongodb
docker exec -it [container name] bash

mongosh
for authentication we switch to the admin database
use admin
db.auth("myUserAdmin", passwordPrompt()) or instead db.auth("myUserAdmin") and then enter the password
now we are authenticated, we can check for example all the databases
show databases
we can see our database from the init script sample_db
use sample_db
we can check for example the number of documents in our sample_collection from the init script
db.sample_collection.countDocuments()

-------------------------------------------------------------


-- pre-commit
every time you update the .pre-commit-config.yaml you have to run pre-commit install to take into account the new steps

-------------------------------------------------------------


--pytest
run pytest -v to get a verbose log

-------------------------------------------------------------

--pyenv
use pyenv to use a specific


-------------------------------------------------------------

--poetry
poetry add to add a new dependency
poetry update when you manually change the toml file and want poetry to solve
dependencies without having to add a new library

if you have a poetry shell(venv) and was created in your local fyle system and you want instead to create one with poetry in your repo you can use:

You just need to type in your shell:

poetry config virtualenvs.in-project true
The virtualenv will be created inside the project path and vscode will recognize.

If you already have created your project, you need to re-create the virtualenv to make it appear in the correct place:

poetry env list  # shows the name of the current environment
poetry env remove <current environment>
poetry install  # will create a new environment using your updated configuration

-------------------------------------------------------------
-tips
to copy to system clipboard from neovim select with visual mode what you need and then "+y this will yank it to the system clipboard

-------------------------------------------------------------
Plans:
ingest data through kafka -> spark streaming -> mongodb
ingest data through some batch method -> postgres
make some transformations using DBT
store those results on a datawarehouse
mask PII data
