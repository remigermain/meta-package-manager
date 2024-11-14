# Copyright Kevin Deldycke <kevin@deldycke.com> and contributors.
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

from __future__ import annotations

import re
import json
from typing import Iterator

from extra_platforms import UNIX_WITHOUT_MACOS

from meta_package_manager.base import Package, PackageManager
from meta_package_manager.capabilities import (
    search_capabilities,
    version_not_implemented,
)


class Fwupdmgr(PackageManager):
    """Documentation: https://fwupd.org/."""

    homepage_url = "https://github.com/fwupd/fwupd"

    platforms = UNIX_WITHOUT_MACOS

    cli_names = ("fwupdmgr", )
    pre_args = ("--json", "--assume-yes")

    @property
    def installed(self) -> Iterator[Package]:
        """Fetch installed packages.

        .. code-block:: shell-session

            ► fwupdmgr get-devices
            {
                "Devices": [
                    {
                        "Name" : "AMD Ryzen 7 4800H with Radeon Graphics",
                        "DeviceId" : "4bde70ba4e39b28f9eab1628f9dd6e6244c03027",
                        "InstanceIds" : [
                            "CPUID\\PRO_0&FAM_17&MOD_60",
                            "CPUID\\PRO_0&FAM_17&MOD_60&STP_1"
                        ],
                        ...
                    },
                    ...
            }
        """
        output = json.loads(self.run_cli("get-devices"))

        for firmware in output["Devices"]:
            yield self.package(
                id=firmware["DeviceId"],
                name=firmware.get("Name"),
                description=firmware.get("Summary"),
                installed_version=firmware.get("Version"),
            )

    @property
    def outdated(self) -> Iterator[Package]:
        """Fetch outdated packages.

        .. code-block:: shell-session

            ► fwupdmgr get-updates
            {
                "Devices": [
                    {
                        "Name" : "AMD Ryzen 7 4800H with Radeon Graphics",
                        "DeviceId" : "4bde70ba4e39b28f9eab1628f9dd6e6244c03027",
                        "InstanceIds" : [
                            "CPUID\\PRO_0&FAM_17&MOD_60",
                            "CPUID\\PRO_0&FAM_17&MOD_60&STP_1"
                        ],
                        ...
                    },
                    ...
            }
        """
        output = json.loads(self.run_cli("get-updates"))

        for firmware in output["Devices"]:
            yield self.package(
                id=firmware["DeviceId"],
                name=firmware.get("Name"),
                description=firmware.get("Summary"),
                installed_version=firmware.get("Version"),
                latest_version=firmware.get("Latest")
            )

    def install(self, package_id: str, version: str | None = None) -> str:
        """Install one package.

        .. code-block:: shell-session

            ► sudo fwupdmgr install 4546446645454
        """
        cmds = ["install", package_id]
        if version:
            cmds.append(version)
        return self.run_cli(*cmds, sudo=True)

    def upgrade_all_cli(self) -> tuple[str, ...]:
        """Generates the CLI to upgrade all packages (default) or only the one provided
        as parameter.

        .. code-block:: shell-session

            ► sudo fwupdmgr uget-pdates
        """
        return self.build_cli("update", sudo=True)

    def sync(self) -> None:
        """Sync package metadata.

        .. code-block:: shell-session

            ► fwupdmgr refresh
        """
        self.run_cli("refresh", "--force")

