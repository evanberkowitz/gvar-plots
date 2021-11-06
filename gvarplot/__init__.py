from .span import vspan, hspan
from .ellipses import ellipse, ellipses
from .errorbar import errorbar
from .mean import mean
from .uncertainty_matrix import uncertainty_matrix

# We can do something smarter than drawing zillions of ellipses
# to get an error band by considering the curve, and finding
# the turning points of distance to the tangent.
# But, for now, this hack suffices.
band=ellipses

