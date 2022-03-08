upgrade-dependencies:
	pip-compile --upgrade requirements.in
	pip-compile --upgrade requirements-dev.in
