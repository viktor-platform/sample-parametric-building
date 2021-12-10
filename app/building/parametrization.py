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
from viktor.parametrization import Parametrization, NumberField, OptionField

_material_options = [
    "Prefab Concrete",
    "Steel Composite",
    "Cross-Laminated-Timber",
    "CLT Composite",
]


class BuildingParametrization(Parametrization):
    """Defines the input fields in left-side of the web UI in the Building entity (Editor)."""
    width = NumberField(
        "Building width",
        suffix="m",
        default=20,
        min=10,
        max=30,
        num_decimals=1,
        variant="slider",
        flex=100,
    )
    length = NumberField(
        "Building Length",
        suffix="m",
        default=30,
        min=20,
        max=40,
        num_decimals=1,
        variant="slider",
        flex=100,
    )
    floor_height = NumberField(
        "Floor Height",
        suffix="m",
        default=3,
        step=0.1,
        min=2.5,
        max=4.0,
        num_decimals=1,
        variant="slider",
        flex=100,
    )
    floors = NumberField(
        "Floors", default=3, min=1, max=10, num_decimals=1, variant="slider", flex=100
    )
    material = OptionField(
        "Construction Material",
        options=_material_options,
        default="Prefab Concrete",
        variant="radio",
        flex=100,
    )
