#
# Plot a 3D Earth with reliefs.
#
import pygmt
import numpy as np
from pygmt.datasets import load_earth_relief

# projection center and size of the Earth
lon0, lat0, size = 170, 30, 15

grid = load_earth_relief(resolution="15m", region=[-180, 180, -90, 90])

fig = pygmt.Figure()
# Add the earth relief
fig.grdimage(grid, projection=f"G{lon0}/{lat0}/{size}c", shading=True, cmap="geo")

# Cut 1/8 of the Earth
x = [lon0 - 45, lon0 - 45, lon0 + 45]
y = [90.0, 0.0, 0.0]
fig.plot(x=x, y=y, fill="darkgray", pen="1p,white")

# Plot Moho
scale = 6300 / 6371  # Moho with a thickness of 71 km
newsize = size * scale
xshift = yshift = size * (1 - scale) / 2.0
fig.shift_origin(xshift=xshift, yshift=yshift)
fig.plot(
    x=x,
    y=y,
    fill="162/99/57",
    pen="0.5p,white",
    projection=f"G{lon0}/{lat0}/{newsize}c",
)
fig.shift_origin(xshift=-xshift, yshift=-yshift)

# Plot CMB
scale = 3480 / 6371
newsize = size * scale
xshift = yshift = size * (1 - scale) / 2.0
fig.shift_origin(xshift=xshift, yshift=yshift)
fig.plot(
    x=x,
    y=y,
    fill="lightgreen",
    pen="0.5p,white",
    projection=f"G{lon0}/{lat0}/{newsize}c",
)
fig.shift_origin(xshift=-xshift, yshift=-yshift)

#### Here, the map projection is switched to linear projection!
# The following codes are used to plot the XYZ axis. mapproject is not wrapped in PyGMT.
with pygmt.clib.Session() as lib:
    with (
        lib.virtualfile_in(x=x, y=y) as vintbl,
        lib.virtualfile_out(kind="dataset") as vouttbl,
    ):
        lib.call_module(
            "mapproject", [vintbl, f"-JG{lon0}/{lat0}/{size}c", "-Rg", f"->{vouttbl}"]
        )
        result = lib.virtualfile_to_dataset(
            output_type="pandas", vfname=vouttbl, column_names=["x", "y"]
        )
        for x0, y0 in zip(result["x"], result["y"]):
            fig.plot(
                x=[x0, size * 0.5],
                y=[y0, size * 0.5],
                projection="x1c",
                region=[0, size, 0, size],
                pen="1p,white@80",
            )

# Plot the inner core
scale = 1221 / 6371
fig.image("3Dball.eps", position=f"JMC+w{size*scale}c")

# Add more labels
fig.text(
    x=size * 0.5,
    y=size * 0.5,
    text="Inner Core",
    font="12p,1,white",
    projection="x1c",
    region=[0, size, 0, size],
)

fig.savefig("3DEarth.jpg")
fig.show()
