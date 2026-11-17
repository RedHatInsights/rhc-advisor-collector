# rhc-advisor-collector

Advisor collector for [rhc](https://github.com/RedHatInsights/rhc). It runs as
`com.redhat.advisor` and collects data with
[insights-core](https://github.com/RedHatInsights/insights-core).

This repository is the upstream for the `rhc-advisor-collector` RPM. The same
spec also builds `rhc-advisor-collector-selinux` from the SELinux policy
sources in [`selinux/`](selinux/). The collection engine stays in insights-core;
this package ships the `rhc_advisor_collector.rhc` adapter that bridges
rhc-collector's executable contract to it. The rhc client stays in the rhc repository.

The collector executable accepts the `collect` subcommand and writes its output
in the working directory set by `rhc-collector`.

## Building

The spec has a single source, this repository (`Source0`), taken from the
`X.Y.Z` tag of the matching version (no `v` prefix — see Package version
below). `make dist` builds it from the local git history; `make srpm` / `make
rpm` depend on it.

```shell
# SRPM only
dnf -y install rpmdevtools
make srpm

# binary RPMs, compiled on this host
dnf -y install rpmdevtools systemd-rpm-macros selinux-policy-devel insights-core-selinux
make rpm

# Source0 only, from the committed tree; GIT_REF= selects another revision
make dist

# remove dist/, srpm/ and rpm/
make clean
```

### Package version

The git tag is the version — bare, no `v` prefix (tags are plain `X.Y.Z`,
matching the default every tool here already assumes a tag's name is its
version). The spec has no hand-bumped `Version:` literal to keep in sync with
it either (`Version: %{version}`, resolved via `rpmbuild --define`). Building
the exact commit tagged `X.Y.Z` produces that real version. Any other build —
plain `main`, a PR branch — stamps a synthetic snapshot version instead
(`0.0.0.dev.g<short commit hash>`), so it can never be mistaken for a real
release. Check what a given build resolves to with:

```shell
make print-version
```

## Requirements

- `rhc`
- `insights-core`
- `insights-core-selinux`, pulled in by `rhc-advisor-collector-selinux` when targeted SELinux policy is installed

## License

Apache-2.0. See [LICENSE](LICENSE).
