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
from typing import Iterator

from extra_platforms import UNIX_WITHOUT_MACOS

from meta_package_manager.base import Package, PackageManager
from meta_package_manager.capabilities import version_not_implemented


class Gnome(PackageManager):
    """Documentation: https://www.gnome.org/"""

    homepage_url = "https://github.com/essembeh/gnome-extensions-cli"

    platforms = UNIX_WITHOUT_MACOS

    requirement = "0.10.3"

    cli_names = ("gext",)
    """
    .. code-block:: shell-session

        ► gext --version
        0.10.3
    """

    pre_args = ("--no-color",)
    list_cmd_regexp = re.compile(r"^.*? (?P<packge_name>.+) \((?P<package_id>\S+)\) (?P<version>v\d+)")

    @property
    def installed(self) -> Iterator[Package]:
        """Fetch installed packages.

        .. code-block:: shell-session

            ► gext --no-color list
            🔵 Background Logo (background-logo@fedorahosted.org) v2 /user
            🔵 Bluetooth Battery Meter (Bluetooth-Battery-Meter@maniacx.github.com) v22 /user
            (...)
        """
        output = self.run_cli("list")

        for package in output.splitlines():
            match = self.list_cmd_regexp.match(package)
            if match:
                packge_name, package_id, version = match.groups()
                yield self.package(id=package_id, name=packge_name, installed_version=version)

    @version_not_implemented
    def install(self, package_id: str, version: str | None = None) -> str:
        """Install one package.

        .. code-block:: shell-session

            ► gext --no-color install xpenguins@mathematical.coffee.gmail.com
        """
        return self.run_cli("install", package_id, sudo=True)

    def upgrade_all_cli(self) -> tuple[str, ...]:
        """Generates the CLI to upgrade all packages (default) or only the one provided
        as parameter.

        .. code-block:: shell-session

            ► gext --no-color update xpenguins@mathematical.coffee.gmail.com
        """
        return self.build_cli("update", sudo=True)

    @version_not_implemented
    def upgrade_one_cli(self, package_id: str, version: str | None = None) -> tuple[str, ...]:
        """Generates the CLI to update all packages (default) or only the one provided
        as parameter.

        .. code-block:: shell-session

            ► gext --no-color upgrade xpenguins@mathematical.coffee.gmail.com
        """
        return self.build_cli("update", package_id, sudo=True)

    def remove(self, package_id: str) -> tuple[str, ...]:
        """Generates the CLI to upgrade all packages (default) or only the one provided
        as parameter.

        .. code-block:: shell-session

            ► gext --no-color uninstall xpenguins@mathematical.coffee.gmail.com
        """
        print(package_id)
        return self.build_cli("uninstall", package_id, sudo=True)
