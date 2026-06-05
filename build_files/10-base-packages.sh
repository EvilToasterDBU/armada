#!/bin/bash
set -euxo pipefail

dnf5 -y install --nogpgcheck \
    --repofrompath 'terra,https://repos.fyralabs.com/terra$releasever' \
    terra-release

dnf5 -y install --setopt=install_weak_deps=False \
    sddm \
    pipewire \
    pipewire-alsa \
    pipewire-pulseaudio \
    wireplumber \
    alsa-lib \
    alsa-ucm \
    alsa-utils \
    qcom-firmware \
    atheros-firmware \
    NetworkManager \
    NetworkManager-wifi \
    iwd \
    wpa_supplicant \
    bluez \
    dbus-broker \
    polkit \
    sudo \
    rsync \
    curl \
    jq \
    lsof \
    unzip \
    evtest \
    btrfs-progs \
    parted \
    gdisk \
    binutils \
    xz \
    dracut \
    dracut-config-generic \
    plymouth \
    plymouth-system-theme \
    plymouth-theme-spinner \
    qt6-qtvirtualkeyboard \
    seatd

dnf5 -y install --setopt=install_weak_deps=False \
    google-noto-sans-cjk-vf-fonts \
    google-noto-sans-thai-vf-fonts \
    google-noto-sans-arabic-vf-fonts \
    google-noto-sans-hebrew-vf-fonts \
    google-noto-sans-devanagari-vf-fonts \
    google-noto-color-emoji-fonts

dnf5 -y install --setopt=install_weak_deps=False \
    plasma-workspace \
    plasma-desktop \
    konsole \
    dolphin
