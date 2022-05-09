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
from munch import Munch
from viktor.core import ViktorController
from viktor.geometry import Group
from viktor.views import DataGroup
from viktor.views import DataItem
from viktor.views import GeometryAndDataResult
from viktor.views import GeometryAndDataView
from .model import calculate_prices
from .model import create_building_geometries
from .model import create_ground_surface
from .parametrization import BuildingParametrization


class BuildingController(ViktorController):
    """Controller class which acts as interface for the Building entity type."""
    label = "Building"
    parametrization = BuildingParametrization(width=20)

    @GeometryAndDataView("3D Model and Shadow Cost", duration_guess=1, default_shadow=False)
    def visualize(self, params: Munch, **kwargs) -> GeometryAndDataResult:
        """Displays a 3D representation of the building, and a DataResult with the shadow price (MKI)"""
        # Create the 3D geometries to be visualized
        ground_surface = create_ground_surface()
        slabs, columns, core = create_building_geometries(params)

        # Calculate the prices for the building geometries and display them using DataItems
        prices = calculate_prices(slabs, columns, core)
        shadow_price_per_element = DataGroup(
            DataItem(
                label="Slabs",
                value=prices["Shadow Price Slabs"],
                prefix="€",
                number_of_decimals=0,
            ),
            DataItem(
                label="Columns",
                value=prices["Shadow Price Columns"],
                prefix="€",
                number_of_decimals=0,
            ),
            DataItem(
                label="Core",
                value=prices["Shadow Price Core"],
                prefix="€",
                number_of_decimals=0,
            ),
        )
        data = DataGroup(
            DataItem(
                label="Shadow Price (MKI)",
                value=prices["Shadow Price (MKI)"],
                prefix="€",
                number_of_decimals=0,
                subgroup=shadow_price_per_element,
            ),
            DataItem(
                label="Shadow Price per m2",
                value=prices["Shadow Price per m2"],
                prefix="€",
                suffix="/m2",
                number_of_decimals=0,
            ),
        )
        return GeometryAndDataResult(
            Group([ground_surface, core, *slabs, *columns]), data
        )
