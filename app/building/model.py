"""Copyright (c) 2021 VIKTOR B.V.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit
persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

VIKTOR B.V. PROVIDES THIS SOFTWARE ON AN "AS IS" BASIS, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT
LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
from typing import Dict
from typing import List
from typing import Tuple

import numpy as np
from munch import Munch

from viktor.core import UserException
from viktor.geometry import Line
from viktor.geometry import Point
from viktor.geometry import Polygon
from viktor.geometry import RectangularExtrusion

from .materials_and_prices import GROUND
from .materials_and_prices import PREFAB_CONCRETE
from .materials_and_prices import SHADOW_PRICE_COLUMN_PER_M
from .materials_and_prices import SHADOW_PRICE_CORE_PER_M2
from .materials_and_prices import SHADOW_PRICE_SLAB_PER_M2
from .materials_and_prices import STEEL
from .materials_and_prices import TIMBER


def determine_materials(selected_material):
    """Determine colors of each part based on material parameter"""
    if selected_material == "Prefab Concrete":
        slab_material = PREFAB_CONCRETE
        column_material = PREFAB_CONCRETE
        core_material = PREFAB_CONCRETE
        column_span = 7.0
    elif selected_material == "Cross-Laminated-Timber":
        slab_material = TIMBER
        column_material = TIMBER
        core_material = TIMBER
        column_span = 6.0
    elif selected_material == "Steel Composite":
        slab_material = STEEL
        column_material = STEEL
        core_material = PREFAB_CONCRETE
        column_span = 8.0
    elif selected_material == "CLT Composite":
        slab_material = PREFAB_CONCRETE
        column_material = TIMBER
        core_material = PREFAB_CONCRETE
        column_span = 5.0
    else:
        raise UserException("Unknown material selected")

    return slab_material, column_material, core_material, column_span


def create_building_geometries(params: Munch) -> Tuple[
    List[RectangularExtrusion],
    List[RectangularExtrusion],
    RectangularExtrusion,
]:
    """Creates the building geometry, including the slabs, columns and core"""
    columns = []
    column_offset = 0.5
    slab_thickness = 0.3
    slab_material, column_material, core_material, column_span = determine_materials(
        params.material
    )

    column_positions_width = np.linspace(
        start=-0.5 * params.width + column_offset,
        stop=0.5 * params.width - column_offset,
        num=round(params.width / column_span + 1),
    )

    column_positions_length = np.linspace(
        start=-0.5 * params.length + column_offset,
        stop=0.5 * params.length - column_offset,
        num=round(params.length / column_span + 1),
    )

    for i in range(params.floors):
        for width_position in column_positions_width:
            for length_position in column_positions_length:
                point_start = Point(
                    width_position,
                    length_position,
                    i * params.floor_height + slab_thickness,
                )
                point_end = Point(
                    width_position, length_position, (i + 1) * params.floor_height
                )
                extrusion_midline = Line(point_start, point_end)
                column = RectangularExtrusion(
                    width=0.5,
                    height=0.5,
                    line=extrusion_midline,
                    material=column_material,
                )
                columns.append(column)

    # Make slabs
    slabs = []
    for i in range(params.floors + 1):
        point_start = Point(0, 0, i * params.floor_height)
        point_end = Point(0, 0, i * params.floor_height + slab_thickness)
        extrusion_midline = Line(point_start, point_end)
        slab = RectangularExtrusion(
            width=params.width,
            height=params.length,
            line=extrusion_midline,
            material=slab_material,
        )
        slabs.append(slab)

    # Make structural core
    core_width, core_length = 6, 8
    point_start = Point(0, 0, slab_thickness)
    point_end = Point(0, 0, params.floors * params.floor_height)
    extrusion_midline = Line(point_start, point_end)
    core = RectangularExtrusion(
        width=core_width,
        height=core_length,
        line=extrusion_midline,
        material=core_material,
    )
    return slabs, columns, core


def create_ground_surface() -> Polygon:
    """Creates the ground surface"""
    # Make ground surface
    x_centre, y_centre = 0, 0  # centre of the circle
    radius = 35  # radius of circle
    points_on_circle = []
    amount_of_points = 100

    for angle in np.linspace(0, 2 * np.pi, amount_of_points, endpoint=False):
        point = Point(x_centre + np.sin(angle) * radius, y_centre + np.cos(angle) * radius)
        points_on_circle.append(point)

    ground_surface = Polygon(points_on_circle, material=GROUND)
    return ground_surface


def calculate_prices(
        slabs: List[RectangularExtrusion],
        columns: List[RectangularExtrusion],
        core: RectangularExtrusion,
) -> Dict[str, float]:
    """Creates a dict containing the shadow prices (MKI)"""
    # Determine shadow cost of slabs
    slab_area_total = 0
    shadow_price_slabs = 0

    for slab in slabs:
        shadow_price_slabs += (
                slab.cross_sectional_area * SHADOW_PRICE_SLAB_PER_M2[slab.material.name]
        )
        slab_area_total += slab.cross_sectional_area

    # Determine shadow cost of columns
    shadow_price_columns = 0
    for column in columns:
        shadow_price_columns += (
                column.length * SHADOW_PRICE_COLUMN_PER_M[column.material.name]
        )

    # Determine shadow cost of core
    core_surface_area = (core.width * 2 + core.height * 2) * core.length
    shadow_price_core = core_surface_area * SHADOW_PRICE_CORE_PER_M2[core.material.name]

    # Determine total shadow price
    shadow_price = shadow_price_slabs + shadow_price_columns + shadow_price_core
    shadow_price_per_m2_total = shadow_price / slab_area_total

    # Present data
    prices_data = {
        "Shadow Price (MKI)": shadow_price,
        "Shadow Price per m2": shadow_price_per_m2_total,
        "Shadow Price Slabs": shadow_price_slabs,
        "Shadow Price Columns": shadow_price_columns,
        "Shadow Price Core": shadow_price_core,
    }

    return prices_data
