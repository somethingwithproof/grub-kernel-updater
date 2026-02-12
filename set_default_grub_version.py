"""Set the highest available kernel version as the GRUB default."""

from __future__ import annotations

import re
import subprocess
from pathlib import Path


class GrubConf:
    """Handles operations related to the GRUB configuration file."""

    def __init__(self, path: str | Path) -> None:
        """Initialize with the path to the GRUB configuration file."""
        self.path = Path(path)
        if not self.path.exists():
            raise FileNotFoundError(f"GRUB configuration file does not exist at {self.path}")

    def get_kernel_versions(self) -> list[str]:
        """Extract kernel versions from the configuration file."""
        pattern = re.compile(r"kernel\s+/boot/vmlinuz-([\d.]+)")
        content = self.path.read_text()
        return [match.group(1) for match in pattern.finditer(content) if match.group(1)]

    def set_default_kernel(self, version: str) -> None:
        """Set the specified kernel version as default in the configuration file."""
        sed_command = ["/usr/bin/sed", "-i.bak", f"s/default=.*/default={version}/", str(self.path)]
        try:
            subprocess.run(sed_command, check=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError("Failed to update the GRUB configuration") from e


class KernelManager:
    """Manages kernel versions for the application."""

    def __init__(self, grub_conf: GrubConf) -> None:
        """Initialize with a GrubConf instance."""
        self.grub_conf = grub_conf

    def set_highest_kernel_as_default(self) -> None:
        """Set the highest kernel version as the default one."""
        versions = self.grub_conf.get_kernel_versions()
        if not versions:
            print("No kernel versions found in GRUB configuration.")
            return

        highest_version = max(versions)
        self.grub_conf.set_default_kernel(highest_version)
        print(f"Successfully set default kernel to {highest_version}.")


def main() -> None:
    """Entry point: set highest kernel as GRUB default."""
    grub_path = "/etc/grub.conf"
    try:
        grub_conf = GrubConf(grub_path)
        kernel_manager = KernelManager(grub_conf)
        kernel_manager.set_highest_kernel_as_default()
    except FileNotFoundError as e:
        print(e)
    except RuntimeError as e:
        print(e)


if __name__ == "__main__":
    main()
