.ONESHELL:

.PHONY : _reset clean test_docker_push test_profiler bootstrap pytest install_dependencies venv install

timestamp=$(`date +Y%m%d`)

venv:
	. venv/bin/activate

clean:
	find . -name '*.pyc' -delete
	find . -name '*.pyo' -delete
	find . -name '*~' -delete
	
docs:
	$(MAKE) -C docs html
	pandoc README.md --from markdown --to rst -s -o README.rst

test_docker_profile: venv
	cp -r "$(PWD)/tests/fixtures/test-traces/atm-ocn" "$(PWD)/traces"; \
	docker build -t esmf-profiler-image . ;\
	docker run -it -v "$(PWD)/traces:/home/traces" esmf-profiler-image esmf-profiler -t /home/traces -n "testdockerpush$(timestamp)" -o /home/traces/output -s;\

test_docker_push: venv
	cp -r "$(PWD)/tests/fixtures/test-traces/atm-ocn" "$(PWD)/traces"; \
	docker build -t esmf-profiler-image . ;\
	docker run -it -v "$(PWD)/traces:/home/traces" esmf-profiler-image esmf-profiler -t /home/traces -n "testdockerprofile$(timestamp)" -o /home/traces/output;\

test_profiler: venv
	esmf-profiler -v -t ./tests/fixtures/test-traces-large/traceout -n "automated-test-$(timestamp)" -o "test$(timestamp)" -p 'https://github.com/ryanlong1004/automatic-succotash'; \

check_build: 
	grep version web/app/package.json;\
	grep version setup.py;\
	

_reset:
	-deactivate
	-rm -rf ./venv
	rm -rf ./dependencies/babeltrace2-2.0.4
	rm -rf ./dependencies/swig-4.0.2
	rm -rf ./dependencies/INSTALL
	

bootstrap: 
	./install_dependencies.sh; \
	./install.sh; \

install: bootstrap
	. ./venv/bin/activate && pip install -e . ; \

pytest: venv
	pip install -e .[test]; \
	python -m pytest; \

test_all: 
	make check_build
	make test_profiler
	make test_docker_push
	make test_docker_profiler
	make pytest
