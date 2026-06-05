#!/usr/bin/env python3
# Minimal Android boot.img (header v0) writer — reproduces the byte layout of
# the ROCKNIX SM8550 KERNEL the ABL boots (base 0x10000000, all load offsets 0,
# pagesize 2048, header_version 0). Only the args make-bootimg.sh passes.
import argparse, hashlib, struct, sys


def os_version_field(ver, patch):
    a, b, c = (list(map(int, ver.split('.'))) + [0, 0, 0])[:3]
    y, m = (list(map(int, patch.split('-'))) + [2000, 1])[:2]
    return (((a << 14) | (b << 7) | c) << 11) | (((y - 2000) << 4) | m)


def pad(blob, n):
    rem = len(blob) % n
    return blob + b'\x00' * ((n - rem) if rem else 0)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--kernel', required=True)
    p.add_argument('--ramdisk', required=True)
    p.add_argument('--cmdline', default='')
    p.add_argument('--base', default='0x10000000')
    p.add_argument('--kernel_offset', default='0')
    p.add_argument('--ramdisk_offset', default='0')
    p.add_argument('--second_offset', default='0')
    p.add_argument('--tags_offset', default='0')
    p.add_argument('--pagesize', default='2048')
    p.add_argument('--header_version', default='0')
    p.add_argument('--os_version', default='12.0.0')
    p.add_argument('--os_patch_level', default='2026-01')
    p.add_argument('-o', '--output', required=True)
    a = p.parse_args()

    base, ps = int(a.base, 0), int(a.pagesize, 0)
    kernel = open(a.kernel, 'rb').read()
    ramdisk = open(a.ramdisk, 'rb').read()
    second = b''

    cmd = a.cmdline.encode()
    if len(cmd) > 512 + 1024:
        sys.exit('mkbootimg: cmdline too long')
    cmdline, extra = cmd[:512], cmd[512:]

    sha = hashlib.sha1()
    for blob in (kernel, ramdisk, second):
        sha.update(blob)
        sha.update(struct.pack('<I', len(blob)))
    img_id = sha.digest()[:20] + b'\x00' * 12   # id[8] u32 = 32 bytes

    hdr = b'ANDROID!'
    hdr += struct.pack('<I', len(kernel))
    hdr += struct.pack('<I', base + int(a.kernel_offset, 0))
    hdr += struct.pack('<I', len(ramdisk))
    hdr += struct.pack('<I', base + int(a.ramdisk_offset, 0))
    hdr += struct.pack('<I', len(second))
    hdr += struct.pack('<I', base + int(a.second_offset, 0))
    hdr += struct.pack('<I', base + int(a.tags_offset, 0))
    hdr += struct.pack('<I', ps)
    hdr += struct.pack('<I', int(a.header_version, 0))
    hdr += struct.pack('<I', os_version_field(a.os_version, a.os_patch_level))
    hdr += b'\x00' * 16                                  # name[16]
    hdr += cmdline + b'\x00' * (512 - len(cmdline))      # cmdline[512]
    hdr += img_id                                        # id[8]
    hdr += extra + b'\x00' * (1024 - len(extra))         # extra_cmdline[1024]

    out = pad(hdr, ps) + pad(kernel, ps) + pad(ramdisk, ps)
    with open(a.output, 'wb') as f:
        f.write(out)


if __name__ == '__main__':
    main()
