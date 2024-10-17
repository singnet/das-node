
bazel-image:
	@./scripts/docker_image_build.sh

bazel-build: bazel-image
	@./scripts/build.sh

wheeler-image:
	@./scripts/build_wheeler_docker_image.sh

wheel: wheeler-image
	@./scripts/run_wheeler.sh

install: wheel
	@pip install ./dist/hyperon_das_atomdb_cpp*.whl --force-reinstall --no-cache-dir

test-cpp:
	@./scripts/bazel_test.sh

test-python:
	@./scripts/python_tests.sh

test-all:
	@./scripts/test_all.sh


