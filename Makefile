docs-html:
	sphinx-build -b html docs/source docs/build

docs-watch:
	watchmedo shell-command --patterns="*.txt;*.rst;*.py" \
              --ignore-pattern='docs/build/*' \
              --recursive \
              --command='make docs-html'
