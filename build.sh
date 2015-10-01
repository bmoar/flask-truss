#!/usr/bin/env bash

PROGRAM_NAME="flask-truss"
PROGRAM_STATIC_NAME="flask-truss-static"
INSTALL_PATH="/usr/local/bin/"
STATIC_FILES_INSTALL_PATH="/srv/www"
DEV_DEPS="python python-dev python-virtualenv python3 python3-dev git"
SYSTEM_DEPS="libpq-dev libffi-dev"

SRC_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

CONTAINER_NAME='flask_truss.lxc'

lxc_config="/var/lib/lxc/$CONTAINER_NAME/config"
lxc_rootfs="/var/lib/lxc/$CONTAINER_NAME/rootfs/"

Lxc_create() {
    name=$1
    if [[ -z $name ]]; then
    cat <<EOF
Lxc_create container_name
default is to use ubuntu template
EOF
    else
        container_template=ubuntu
        auth_keys=".ssh/authorized_keys"
        sudo -E lxc-create -t $container_template -n $name -- -u $SUDO_USER -S $HOME/$auth_keys
        sudo -E lxc-start -d -n $name
    fi
}

install_deps() {
    if [[ "$OSTYPE" == "linux-gnu" ]]; then
        sudo apt-get update
        sudo apt-get install -y lxc liblxc1 python3-lxc
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo 'sorry lxc does not work on OSX, use a vagrant VM'
        exit 1
    fi
}

bootstrap() {
    Lxc_create $CONTAINER_NAME
    sudo chroot $lxc_rootfs sudo apt-get update
    sudo chroot $lxc_rootfs sudo apt-get install -y $DEV_DEPS
    sudo chroot $lxc_rootfs sudo apt-get install -y $SYSTEM_DEPS

    repo_mount="lxc.mount.entry = $SRC_DIR home/$SUDO_USER/$PROGRAM_NAME none bind,create=dir 0 0"
    if ! grep -q "$repo_mount" "$lxc_config"; then
        echo "$repo_mount" | sudo tee -a $lxc_config
    fi
    sudo lxc-stop -n "$CONTAINER_NAME"
    sudo lxc-start -d -n "$CONTAINER_NAME"
}

clean() {
    # Clean up packaging artifacts
    rm -rf $SRC_DIR/build
    rm -rf $SRC_DIR/dist
    rm -rf $SRC_DIR/*.egg-info
    rm -rf $SRC_DIR/*.deb
    rm -rf $INSTALL_PATH/$PROGRAM_NAME
    rm -rf $STATIC_FILES_INSTALL_PATH/$PROGRAM_STATIC_NAME
    find . -name '*.pyc' -delete
}

usage() {
    msgs=(
        'build.sh option [arg]'
        '-b | --bootstrap - create minimal dev lxc container'
    )

    for msg in "${msgs[@]}"; do
        echo $msg
    done

    exit 1
}

main() {
    options=$@
    args=($options)
    i=0

    for arg in $options; do
        i=$(( $i + 1 ))

        case $arg in
            -b|--bootstrap|bootstrap)
                bootstrap
                break
                ;;
            *)
                usage
                break
                ;;
        esac
    done
}

main $@
