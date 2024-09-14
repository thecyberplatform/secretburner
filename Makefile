help:
	@echo  "Usage:"
	@echo  ""
	@echo  "@command :  make up"
	@echo  "@desc    :  Brings up all docker-compose services with force recreate."
	@echo  "@example :  make up"
	@echo  "@example :  make up apps=\"secretburner-api secretburner-ui\""
	@echo  ""
	@echo  "@command :  make down"
	@echo  "@desc    :  Brings down all docker-compose services."
	@echo  ""
	@echo  "@command :  make build"
	@echo  "@desc    :  Builds all the docker-compose services; without bringing them up."
	@echo  "@example :  make build"
	@echo  "@example :  make build apps=\"secretburner-api secretburner-ui\""
	@echo  ""
	@echo  "@command :  make startapp"
	@echo  "@desc    :  Generates a Django app module in app/api."
	@echo  "@example :  make startapp app=\"name_of_app\""
	@echo  ""
	@echo  "@command :  make migrations"
	@echo  "@desc    :  Runs Django \`makemigrations\` command to generate model change migration files."
	@echo  ""
	@echo  "@command :  make migrate"
	@echo  "@desc    :  Runs Django `migrate` command to apply model changes."
	@echo  ""
	@echo  "@command :  make emptyMigration"
	@echo  "@desc    :  Generates a an empty migration file for a given Django app label."
	@echo  "@example :  make emptyMigration app=\"name_of_app\""
	@echo  ""
	@echo  "@command :  make apiTest"
	@echo  "@desc    :  Runs Django test suite. (optionally) Test only a single module using the \`mod\` argument."
	@echo  "@example :  make apiTest"
	@echo  "@example :  make apiTest mod=\"secret.tests\""
	@echo  ""
	@echo  "@command :  make npmi"
	@echo  "@desc    :  Runs NPM install on the UI service."
	@echo  "@example :  make npmi"
	@echo  "@example :  make npmi app=\"lodash\""
	@echo  ""
	@echo  "@command :  make npmr"
	@echo  "@desc    :  Runs NPM uninstall on the UI service."
	@echo  "@example :  make npmr app=\"lodash\""
	@echo  ""
	@echo  "@command :  make npmu"
	@echo  "@desc    :  Runs NPM update on the UI service."
	@echo  "@example :  make npmu"
	@echo  "@example :  make npmu app=\"lodash\""
	@echo  ""
	@echo  "@command :  make npmfix"
	@echo  "@desc    :  Runs NPM audit fix"
	@echo  "@example :  make npmfix"
	@echo  "@example :  make npmfix args=\"--force\""
	@echo  ""
	@echo  "@command :  make packageUI"
	@echo  "@desc    :  Builds a deployable distribution of the UI service."
	@echo  "@example :  make packageUI"
	@echo  ""
	@echo  "@command :  make vulnScan"
	@echo  "@desc    :  Runs Trivy vulnerability scanner on all docker-compose services."
	@echo  "@example :  make vulnScan"

up:
	docker-compose -f deploy/docker/docker-compose.local.yml up -d --force-recreate --remove-orphans $(apps)

down:
	docker-compose -f deploy/docker/docker-compose.local.yml down

build:
	docker-compose -f deploy/docker/docker-compose.local.yml build --progress=plain $(args) $(apps)

startapp:
	docker-compose -f deploy/docker/docker-compose.local.yml run --rm secretburner-api python manage.py startapp $(app)

migrations:
	docker-compose -f deploy/docker/docker-compose.local.yml run --rm secretburner-api python manage.py makemigrations

migrate:
	docker-compose -f deploy/docker/docker-compose.local.yml run --rm secretburner-api python manage.py migrate

emptyMigration:
	docker-compose -f deploy/docker/docker-compose.local.yml run --rm secretburner-api python manage.py makemigrations --empty $(app)

apiRun:
	docker-compose -f deploy/docker/docker-compose.local.yml run --rm secretburner-api $(r)

apiTest:
	docker-compose -f deploy/docker/docker-compose.local.yml run --rm secretburner-api python manage.py test -v 3 $(mod)

pyCoverage:
	docker-compose -f deploy/docker/docker-compose.local.yml up -d
	docker-compose -f deploy/docker/docker-compose.local.yml run --rm secretburner-api rm -rf /app/coverage/
	docker-compose -f deploy/docker/docker-compose.local.yml run --rm secretburner-api coverage run --source='/app/' /app/manage.py test -v 3

pyCoverageHtml:
	docker-compose -f deploy/docker/docker-compose.local.yml run --rm secretburner-api coverage html --data-file=/app/.coverage -d /app/coverage/

uiRun:
	docker-compose -f deploy/docker/docker-compose.local.yml run --rm secretburner-ui $(r)

npmi:
	docker-compose -f deploy/docker/docker-compose.local.yml run --rm secretburner-ui npm install $(app)

npmr:
	docker-compose -f deploy/docker/docker-compose.local.yml run --rm secretburner-ui npm uninstall -S $(app)

npmu:
	docker-compose -f deploy/docker/docker-compose.local.yml run --rm secretburner-ui npm update

npmfix:
	docker-compose -f deploy/docker/docker-compose.local.yml run --rm secretburner-ui npm audit fix $(args)

packageUI:
	docker-compose -f deploy/docker/docker-compose.local.yml run --rm secretburner-ui quasar build

vulnScan:
	docker run aquasec/trivy image secretburner-ui:latest
	docker run aquasec/trivy image secretburner-api:latest
	docker run aquasec/trivy image secretburner-db:latest
	docker run aquasec/trivy image secretburner-proxy:latest
