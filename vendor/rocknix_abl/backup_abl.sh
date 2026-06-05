#!/bin/bash
# SPDX-License-Identifier: GPL-2.0
# From ROCKNIX (https://github.com/ROCKNIX/abl), (c) ROCKNIX contributors.

# Backup abl_a and abl_b

dd if=/dev/block/by-name/abl_a of="/sdcard/rocknix_abl/abl_a.img" bs=1M
dd if=/dev/block/by-name/abl_b of="/sdcard/rocknix_abl/abl_b.img" bs=1M
