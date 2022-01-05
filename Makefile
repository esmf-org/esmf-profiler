.PHONY : _reset clean test_docker_push test_profiler bootstrap pytest

clean:
	find . -name '*.pyc' -delete
	find . -name '*.pyo' -delete
	find . -name '*~' -delete
	
docs:
	$(MAKE) -C docs html
	pandoc README.md --from markdown --to rst -s -o README.rst

test_docker_push:
	cp -r "$(PWD)/tests/fixtures/test-traces/atm-ocn" "$(PWD)/traces"
	docker build -t esmf-profiler-image .
	docker run -it -v "$(PWD)/traces:/home/traces" esmf-profiler-image esmf-profiler -t /home/traces -n "testdockerpush" -o /home/traces/output

test_profiler:
	esmf-profiler -v -t ./tests/fixtures/test-traces-large/traceout -n "test-_-20211122" -o "test20211122" -p 'https://github.com/ryanlong1004/automatic-succotash'

_reset:
	-deactivate
	-rm -rf ./venv
	rm -rf ./dependencies/babeltrace2-2.0.4
	rm -rf ./dependencies/swig-4.0.2
	rm -rf ./dependencies/INSTALL
	

bootstrap: 
	./install_dependencies.sh 
	./install.sh 
	source ./venv/bin/activate && pip install -e .

pytest:
	./install_dependencies.sh && ./install.sh && source ./venv/bin/activate && pip install -e .[test]
	python -m pytest

test_all: bootstrap
	test_profiler 
	test_docker_push
	pytest