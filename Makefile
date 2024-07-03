build:
	python -m nuitka --follow-imports cmd.py --onefile --show-scons --no-deployment-flag=self-execution --show-progress --output-dir=.build_tmp --verbose --output-filename=lsfeye --low-memory
