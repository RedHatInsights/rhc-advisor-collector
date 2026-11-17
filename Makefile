NAME := rhc-advisor-collector

# Revision packed as Source0.
GIT_REF ?= HEAD

# Effective version for this build. The git tag IS the version, bare (no `v`
# prefix -- tags are plain X.Y.Z, matching Packit's own default assumption
# that a tag's name is its version, so no upstream_tag_template is needed).
GIT_EXACT_TAG := $(shell git describe --tags --exact-match --match '[0-9]*' $(GIT_REF) 2>/dev/null)

ifneq ($(GIT_EXACT_TAG),)
VERSION := $(GIT_EXACT_TAG)
else
VERSION := 0.0.0.dev.g$(shell git rev-parse --short $(GIT_REF) 2>/dev/null)
endif

TARBALL := dist/$(NAME)-$(VERSION).tar.gz
SRCDIR := $(NAME)-$(VERSION)

.PHONY: dist srpm rpm clean print-version

# For .packit.yaml's get-current-version action, so the version packit's own
# build resolves to matches what create-archive (make dist) already named
# the tarball.
print-version:
	@echo $(VERSION)

dist: $(TARBALL)

$(TARBALL):
	mkdir -p dist
	git archive --format=tar.gz --prefix=$(SRCDIR)/ -o $@ $(GIT_REF)

srpm: dist
	rpmbuild --define="version $(VERSION)" -bs \
		--define="_sourcedir $(abspath dist)" \
		--define="_srcrpmdir $(abspath srpm)" \
		$(NAME).spec

rpm: dist
	rpmbuild --define="version $(VERSION)" -bb \
		--define="_sourcedir $(abspath dist)" \
		--define="_rpmdir $(abspath rpm)" \
		$(NAME).spec

clean:
	rm -rf dist srpm rpm
