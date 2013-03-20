install_dev:
	"pip install -e ."
	"pip install -r requirements-dev.txt"

test:
	coverage run --branch --source=simpleimages -m django-mini -a simpleimages -a simpleimages.test --test-runner 'discover_runner.DiscoverRunner' test
