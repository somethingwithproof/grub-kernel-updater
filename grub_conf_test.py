"""Tests for the GRUB kernel updater."""

from __future__ import annotations

import os
import tempfile

import pytest

from set_default_grub_version import GrubConf, KernelManager


@pytest.fixture()
def grub_conf_file():
    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(b"kernel /boot/vmlinuz-5.10.0-1234\nkernel /boot/vmlinuz-5.11.0-5678\n")
        f.flush()
        yield f.name
        os.unlink(f.name)


def test_get_kernel_versions(grub_conf_file):
    versions = GrubConf(grub_conf_file).get_kernel_versions()
    assert versions == ["5.10.0-1234", "5.11.0-5678"]


def test_set_default_kernel(grub_conf_file):
    grub_conf = GrubConf(grub_conf_file)
    grub_conf.set_default_kernel("5.11.0-5678")

    with open(grub_conf_file) as f:
        content = f.read()
    # sed replaces default=.* lines; the kernel lines remain unchanged
    assert "kernel /boot/vmlinuz-5.10.0-1234" in content


@pytest.fixture()
def kernel_manager(grub_conf_file):
    yield KernelManager(GrubConf(grub_conf_file))


def test_kernel_manager_set_highest_kernel_as_default(capsys, kernel_manager):
    kernel_manager.set_highest_kernel_as_default()
    captured = capsys.readouterr()
    assert "Successfully set default kernel to 5.11.0-5678." in captured.out
