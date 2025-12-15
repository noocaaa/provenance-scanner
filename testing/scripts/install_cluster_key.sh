#!/bin/bash
set -e

CLUSTER_PUB_KEY="/vagrant/cluster_key.pub"
SSH_DIR="/home/vagrant/.ssh"
AUTHORIZED_KEYS="$SSH_DIR/authorized_keys"

mkdir -p "$SSH_DIR"
chmod 700 "$SSH_DIR"

touch "$AUTHORIZED_KEYS"
chmod 600 "$AUTHORIZED_KEYS"
chown -R vagrant:vagrant "$SSH_DIR"

# Añadir la clave solo si no existe
grep -qxF "$(cat $CLUSTER_PUB_KEY)" "$AUTHORIZED_KEYS" || \
  cat "$CLUSTER_PUB_KEY" >> "$AUTHORIZED_KEYS"
