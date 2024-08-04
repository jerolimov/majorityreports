all: update-openapi update-dashboard-types

update-openapi:
	cd api && make install update-openapi

update-dashboard-types:
	cd dashboard && make update-types
