PYTHON_FILE := .pdm-python
build:
	[ -f "${PYTHON_FILE}" ] && $(shell cat "${PYTHON_FILE}") -m nuitka --follow-imports cmd.py --onefile --show-scons --no-deployment-flag=self-execution --show-progress --output-dir=.build_tmp --verbose --output-filename=lsfeye --low-memory --jobs=4
