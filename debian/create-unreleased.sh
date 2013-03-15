#!/bin/bash

usage() {
    cat <<EOT
Usage: $0 <path to git tree>

This script will generate a dev tarball of cms from a git tree.
All desired changes must be committed to the tree.
DO NOT USE THIS FOR RELEASE PACKAGES.
EOT
    exit 2
}

error() {
    echo "$@" 1>&2
    exit 1
}

[ -z "$1" ] && usage

GIT_DIR=$1

test -d "$GIT_DIR" || error "Path '$GIT_DIR' does not exist."
REV=$(cd "$GIT_DIR" && git rev-parse --short HEAD) || error "$GIT_DIR is not a git repo?"
RELEASE=$(cd "$GIT_DIR/docs" && python -c 'import conf ; print conf.release')
DATE=$(TZ=UTC date --date="@$(cd "$GIT_DIR" && git log -1 --format=%ct $REV)" +%Y%m%d~%H%M%S)

# Make the version number sortable if a pre-release.
case "$RELEASE" in
    *[0-9]pre) RELEASE=${RELEASE%pre}~pre
esac

ORIGVERSION="${RELEASE}~git$DATE+$REV"

dch --force-bad-version -v "${ORIGVERSION}-1" "New upstream git snapshot."

TARBALL=../cms_${ORIGVERSION}.orig.tar.gz
echo "Writing archive to $TARBALL"
(cd "$GIT_DIR" && git archive $REV) | gzip --best > "$TARBALL"

set -x
#rm -rf src
#mkdir src
#cd src && \
tar xzf $TARBALL

echo "Run the following command to build the package."
echo dpkg-buildpackage -us -uc
