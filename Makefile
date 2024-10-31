
# C++ commands:
cpp-image:
	@./scripts/cpp_image.sh

cpp-build:
	@./scripts/cpp_build.sh

cpp-test:
	@./scripts/cpp_test.sh

# Python commands
wheeler-image:
	@./scripts/wheeler_image.sh

wheeler-build: 
	@./scripts/wheeler_build.sh

wheeler-test:
	@./scripts/wheeler_test.sh

install:
	@python3 -m pip install ./dist/hyperon_das_node*.whl --force-reinstall --no-cache-dir

# Run all tests
test-all: test-cpp test-python

# Clean docker volumes and build directories
clean:
	@docker volume rm bazel_cache
	@rm -rf src/bazel-* bazel_assets build dist
