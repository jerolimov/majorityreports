install:
	yarn install

build:
	yarn build:backend
	# yarn tsc:full

lint:
	# yarn lint:all

test:
	# yarn test:all

update-types:
	if [ ! -d node_modules ]; then yarn install; fi
	cd plugins/majorityreports-common && yarn run update-types
