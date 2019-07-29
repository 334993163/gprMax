# Copyright (C) 2015-2019: The University of Edinburgh
#                 Authors: Craig Warren and Antonis Giannopoulos
#
# This file is part of gprMax.
#
# gprMax is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# gprMax is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with gprMax.  If not, see <http://www.gnu.org/licenses/>.

from .base import SubGridBase
from .hsg_fields_updates_ext import cython_update_is
from .hsg_fields_updates_ext import cython_update_electric_os
from .hsg_fields_updates_ext import cython_update_magnetic_os
from ..utilities import human_size
from ..utilities import memory_usage

from colorama import init, Fore, Style
init()


class SubGridHSG(SubGridBase):

    gridtype = '3DSUBGRID'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.gridtype = SubGridHSG.gridtype

        # upper and lower indices for the OS.
        self.i_l = self.i0 - self.is_os_sep
        self.i_u = self.i1 + self.is_os_sep
        self.j_l = self.j0 - self.is_os_sep
        self.j_u = self.j1 + self.is_os_sep
        self.k_l = self.k0 - self.is_os_sep
        self.k_u = self.k1 + self.is_os_sep

    def update_magnetic_is(self, precursors):
        """Apply the incident field corrections to the subgrid fields at the IS.

        Args:
              precursors (PrecursorNodes): PrecursorNodes are the incident
              fields calculated at the correct time and position.
        """
        # bottom and top faces
        cython_update_is(self.nwx, self.nwy, self.nwz, self.updatecoeffsH, self.ID, self.n_boundary_cells, -1, self.nwx, self.nwy + 1, self.nwz, 1, self.Hy, precursors.ex_bottom, precursors.ex_top, self.IDlookup['Hy'], 1, -1, 3, self.nthreads)
        cython_update_is(self.nwx, self.nwy, self.nwz, self.updatecoeffsH, self.ID, self.n_boundary_cells, -1, self.nwx + 1, self.nwy, self.nwz, 1, self.Hx, precursors.ey_bottom, precursors.ey_top, self.IDlookup['Hx'], -1, 1, 3, self.nthreads)

        # left and right faces
        cython_update_is(self.nwx, self.nwy, self.nwz, self.updatecoeffsH, self.ID, self.n_boundary_cells, -1, self.nwy, self.nwz + 1, self.nwx, 2, self.Hz, precursors.ey_left, precursors.ey_right, self.IDlookup['Hz'], 1, -1, 1, self.nthreads)
        cython_update_is(self.nwx, self.nwy, self.nwz, self.updatecoeffsH, self.ID, self.n_boundary_cells, -1, self.nwy + 1, self.nwz, self.nwx, 2, self.Hy, precursors.ez_left, precursors.ez_right, self.IDlookup['Hy'], -1, 1, 1, self.nthreads)

        # front and back faces
        cython_update_is(self.nwx, self.nwy, self.nwz, self.updatecoeffsH, self.ID, self.n_boundary_cells, -1, self.nwx, self.nwz + 1, self.nwy, 3, self.Hz, precursors.ex_front, precursors.ex_back, self.IDlookup['Hz'], -1, 1, 2, self.nthreads)
        cython_update_is(self.nwx, self.nwy, self.nwz, self.updatecoeffsH, self.ID, self.n_boundary_cells, -1, self.nwx + 1, self.nwz, self.nwy, 3, self.Hx, precursors.ez_front, precursors.ez_back, self.IDlookup['Hx'], 1, -1, 2, self.nthreads)

    def update_electric_is(self, precursors):
        """Apply the incident field corrections to the subgrid fields at the IS.

        Args:
              precursors (PrecursorNodes): PrecursorNodes are the incident
              fields calculated at the correct time and position.
        """
        # bottom and top faces
        cython_update_is(self.nwx, self.nwy, self.nwz, self.updatecoeffsE, self.ID, self.n_boundary_cells, 0, self.nwx, self.nwy + 1, self.nwz, 1, self.Ex, precursors.hy_bottom, precursors.hy_top, self.IDlookup['Ex'], 1, -1, 3, self.nthreads)
        cython_update_is(self.nwx, self.nwy, self.nwz, self.updatecoeffsE, self.ID, self.n_boundary_cells, 0, self.nwx + 1, self.nwy, self.nwz, 1, self.Ey, precursors.hx_bottom, precursors.hx_top, self.IDlookup['Ey'], -1, 1, 3, self.nthreads)

        # left and right faces
        cython_update_is(self.nwx, self.nwy, self.nwz, self.updatecoeffsE, self.ID, self.n_boundary_cells, 0, self.nwy, self.nwz + 1, self.nwx, 2, self.Ey, precursors.hz_left, precursors.hz_right, self.IDlookup['Ey'], 1, -1, 1, self.nthreads)
        cython_update_is(self.nwx, self.nwy, self.nwz, self.updatecoeffsE, self.ID, self.n_boundary_cells, 0, self.nwy + 1, self.nwz, self.nwx, 2, self.Ez, precursors.hy_left, precursors.hy_right, self.IDlookup['Ez'], -1, 1, 1, self.nthreads)

        # front and back faces
        cython_update_is(self.nwx, self.nwy, self.nwz, self.updatecoeffsE, self.ID, self.n_boundary_cells, 0, self.nwx, self.nwz + 1, self.nwy, 3, self.Ex, precursors.hz_front, precursors.hz_back, self.IDlookup['Ex'], -1, 1, 2, self.nthreads)
        cython_update_is(self.nwx, self.nwy, self.nwz, self.updatecoeffsE, self.ID, self.n_boundary_cells, 0, self.nwx + 1, self.nwz, self.nwy, 3, self.Ez, precursors.hx_front, precursors.hx_back, self.IDlookup['Ez'], 1, -1, 2, self.nthreads)

    def update_electric_os(self, main_grid):
        """Apply the incident field corrections to the main grid fields at the OS.

        Main grid fields are collocated with subgrid fields therefore
        precursor fields are not required.

        Args:
              main_grid (FDTDGrid): main fdtd solver grid
        """
        # front and back
        cython_update_electric_os(main_grid.updatecoeffsE, main_grid.ID, 3, self.i_l, self.i_u, self.k_l, self.k_u + 1, self.j_l, self.j_u, self.nwy, main_grid.IDlookup['Ex'], main_grid.Ex, self.Hz, 2, 1, -1, 1, self.ratio, self.is_os_sep, self.n_boundary_cells, main_grid.nthreads)
        cython_update_electric_os(main_grid.updatecoeffsE, main_grid.ID, 3, self.i_l, self.i_u + 1, self.k_l, self.k_u, self.j_l, self.j_u, self.nwy, main_grid.IDlookup['Ez'], main_grid.Ez, self.Hx, 2, -1, 1, 0, self.ratio, self.is_os_sep, self.n_boundary_cells, main_grid.nthreads)

        # Left and Right
        cython_update_electric_os(main_grid.updatecoeffsE, main_grid.ID, 2, self.j_l, self.j_u, self.k_l, self.k_u + 1, self.i_l, self.i_u, self.nwx, main_grid.IDlookup['Ey'], main_grid.Ey, self.Hz, 1, -1, 1, 1, self.ratio, self.is_os_sep, self.n_boundary_cells, main_grid.nthreads)
        cython_update_electric_os(main_grid.updatecoeffsE, main_grid.ID, 2, self.j_l, self.j_u + 1, self.k_l, self.k_u, self.i_l, self.i_u, self.nwx, main_grid.IDlookup['Ez'], main_grid.Ez, self.Hy, 1, 1, -1, 0, self.ratio, self.is_os_sep, self.n_boundary_cells, main_grid.nthreads)

        # Bottom and Top
        cython_update_electric_os(main_grid.updatecoeffsE, main_grid.ID, 1, self.i_l, self.i_u, self.j_l, self.j_u + 1, self.k_l, self.k_u, self.nwz, main_grid.IDlookup['Ex'], main_grid.Ex, self.Hy, 3, -1, 1, 1, self.ratio, self.is_os_sep, self.n_boundary_cells, main_grid.nthreads)
        cython_update_electric_os(main_grid.updatecoeffsE, main_grid.ID, 1, self.i_l, self.i_u + 1, self.j_l, self.j_u, self.k_l, self.k_u, self.nwz, main_grid.IDlookup['Ey'], main_grid.Ey, self.Hx, 3, 1, -1, 0, self.ratio, self.is_os_sep, self.n_boundary_cells, main_grid.nthreads)

    def update_magnetic_os(self, main_grid):
        """Apply the incident field corrections to the main grid fields at the OS.

        Main grid fields are collocated with subgrid fields therefore
        precursor fields are not required.

        Args:
              main_grid (FDTDGrid): main fdtd solver grid
        """

        # Front and back
        cython_update_magnetic_os(main_grid.updatecoeffsH, main_grid.ID, 3, self.i_l, self.i_u, self.k_l, self.k_u + 1, self.j_l - 1, self.j_u, self.nwy, main_grid.IDlookup['Hz'], main_grid.Hz, self.Ex, 2, 1, -1, 1, self.ratio, self.is_os_sep, self.n_boundary_cells, main_grid.nthreads)
        cython_update_magnetic_os(main_grid.updatecoeffsH, main_grid.ID, 3, self.i_l, self.i_u + 1, self.k_l, self.k_u, self.j_l - 1, self.j_u, self.nwy, main_grid.IDlookup['Hx'], main_grid.Hx, self.Ez, 2, -1, 1, 0, self.ratio, self.is_os_sep, self.n_boundary_cells, main_grid.nthreads)

        # Left and Right
        cython_update_magnetic_os(main_grid.updatecoeffsH, main_grid.ID, 2, self.j_l, self.j_u, self.k_l, self.k_u + 1, self.i_l - 1, self.i_u, self.nwx, main_grid.IDlookup['Hz'], main_grid.Hz, self.Ey, 1, -1, 1, 1, self.ratio, self.is_os_sep, self.n_boundary_cells, main_grid.nthreads)
        cython_update_magnetic_os(main_grid.updatecoeffsH, main_grid.ID, 2, self.j_l, self.j_u + 1, self.k_l, self.k_u, self.i_l - 1, self.i_u, self.nwx, main_grid.IDlookup['Hy'], main_grid.Hy, self.Ez, 1, 1, -1, 0, self.ratio, self.is_os_sep, self.n_boundary_cells, main_grid.nthreads)

        # bottom and top
        cython_update_magnetic_os(main_grid.updatecoeffsH, main_grid.ID, 1, self.i_l, self.i_u, self.j_l, self.j_u + 1, self.k_l - 1, self.k_u, self.nwz, main_grid.IDlookup['Hy'], main_grid.Hy, self.Ex, 3, -1, 1, 1, self.ratio, self.is_os_sep, self.n_boundary_cells, main_grid.nthreads)
        cython_update_magnetic_os(main_grid.updatecoeffsH, main_grid.ID, 1, self.i_l, self.i_u + 1, self.j_l, self.j_u, self.k_l - 1, self.k_u, self.nwz, main_grid.IDlookup['Hx'], main_grid.Hx, self.Ey, 3, 1, -1, 0, self.ratio, self.is_os_sep, self.n_boundary_cells, main_grid.nthreads)

    def __str__(self):
        s = '\n'
        s += Fore.CYAN
        s += 'Sub Grid HSG\n'
        s += 'Name: {}\n'.format(self.name)
        s += 'dx, dy, dz: {}m {}m {}m\n'.format(self.dx, self.dy, self.dz)
        s += 'dt: {}s\n'.format(self.dt)
        s += 'Memory Estimate: {}\n'.format(human_size(memory_usage(self)))
        s += 'Position: ({}m, {}m, {}m), ({}m, {}m, {}m)\n'.format(self.x1,
                                                                   self.y1,
                                                                   self.z1,
                                                                   self.x2,
                                                                   self.y2,
                                                                   self.z2)
        s += 'Main Grid Indices: lower left({}, {}, {}), upper right({}, {}, {})\n'.format(self.i0, self.j0, self.k0, self.i1, self.j1, self.k1)
        s += 'Total Cells: {} {} {}\n'.format(self.nx, self.ny, self.nz)
        s += 'Working Region Cells: {} {} {}\n'.format(self.nwx,
                                                       self.nwy,
                                                       self.nwz)
        for h in self.hertziandipoles:
            s += 'Hertizian dipole: {} {} {}\n'.format(h.xcoord,
                                                       h.ycoord,
                                                       h.zcoord)
            s += str([x for x in self.waveforms
                      if x.ID == h.waveformID][0]) + '\n'
        for r in self.rxs:
            s += 'Receiver: {} {} {}\n'.format(r.xcoord, r.ycoord, r.zcoord)

        for tl in self.transmissionlines:
            s += 'Transmission Line: {} {} {}\n'.format(tl.xcoord, tl.ycoord, tl.zcoord)
            s += str([x for x in self.waveforms
                      if x.ID == tl.waveformID][0]) + '\n'
        s += Style.RESET_ALL
        return s
