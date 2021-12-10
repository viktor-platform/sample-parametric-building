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
from viktor.core import Color
from viktor.geometry import Material

SHADOW_PRICE_SLAB_PER_M2 = {
    "Prefab Concrete": 12.8,
    "Cross-Laminated-Timber": 0.9,
    "Steel Composite": 10.2,
}
SHADOW_PRICE_COLUMN_PER_M = {
    "Prefab Concrete": 17.1,
    "Cross-Laminated-Timber": 0.7,
    "Steel Composite": 9.0,
}
SHADOW_PRICE_CORE_PER_M2 = {
    "Prefab Concrete": 6.9,
    "Cross-Laminated-Timber": 0.9
}

PREFAB_CONCRETE = Material("Prefab Concrete", color=Color(220, 220, 220))
TIMBER = Material("Cross-Laminated-Timber", color=Color(250, 200, 150))
STEEL = Material("Steel Composite", color=Color(100, 100, 100))
GROUND = Material("ground green", color=Color(200, 250, 155))
