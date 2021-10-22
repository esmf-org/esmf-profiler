docker build .

docker run -it -v $(pwd)/traces:/home/traces test9 esmf-profiler -t /home/traces -n 'test' -o /home/traces/output