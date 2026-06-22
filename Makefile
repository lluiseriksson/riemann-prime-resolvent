.PHONY: bootstrap build verify oracle audit paper clean package

bootstrap:
	./scripts/bootstrap.sh

build:
	lake build

verify:
	./scripts/verify.sh

oracle:
	lake env lean oracle_check.lean

audit:
	python3 scripts/check_consistency.py

paper:
	$(MAKE) -C paper

clean:
	rm -rf .lake/build
	$(MAKE) -C paper clean

package:
	./scripts/package_release.sh dev
