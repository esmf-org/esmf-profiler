.ONESHELL:

.PHONY : _reset clean test_docker_push test_profiler bootstrap pytest install_dependencies venv install test



venv:
	cd ..;\
	. venv/bin/activate

clean:
	cd ..;\
	find . -name '*.pyc' -delete
	find . -name '*.pyo' -delete
	find . -name '*~' -delete
	
docs:
	$(MAKE) -C docs html
	pandoc README.md --from markdown --to rst -s -o README.rst

test_docker_profiler: venv
	timestamp=$(date +%Y%m%d);\
	cd ..;\
	cp -r "$(PWD)/fixtures/test-traces/atm-ocn" "$(PWD)/traces"; \
	docker build --build-arg SOURCE_BRANCH_NAME=main -t esmf-profiler-image . ;\
	docker run -it -v "$(PWD)/traces:/home/traces" esmf-profiler-image esmf-profiler -t /home/traces -n "testdockerpush$(timestamp)" -o /home/traces/output;\

test_profiler: venv
	timestamp=$(date +%Y%m%d);\
	cd ..;\
	esmf-profiler -v -t ./tests/fixtures/test-traces/atm-ocn -n "automated-test-$(timestamp)" -o "test$(timestamp)" -p 'https://github.com/ryanlong1004/automatic-succotash'; \

check_build: 
	cd ..;\
	grep version ./web/app/package.json;\
	grep version ./setup.py;\
	

_reset:
	cd ..
	-deactivate
	-rm -rf ./venv
	rm -rf ./dependencies/babeltrace2-2.0.4
	rm -rf ./dependencies/swig-4.0.2
	rm -rf ./dependencies/INSTALL
	

bootstrap: 
	cd ..;\
	./install_dependencies.sh; \
	./install.sh; \

install: bootstrap
	cd ..;\
	. ./venv/bin/activate && pip install -e .; \

pytest: venv
	cd ..;\
	pip install -e .[test]; \
	python -m pytest; \

test_all: 
	make test_profiler
	make test_docker_profiler
	make pytest
	make check_build
