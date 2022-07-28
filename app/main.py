'''
Proceedurally create video test patters for LED and Projected video Projects

Tech Stack: Python3 pillow fast-api
'''
from fastapi import FastAPI, Response, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from PIL import Image, ImageDraw

app = FastAPI()

origins = ["*"] # Configured for public API

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Video Grid Maker - use /docs"}

@app.get("/grid")
async def grid(width, height, background_color, border_color, grid_color, grid_px_size):
    image = Image.new('RGBA', size=(width, height), color=background_color)
    # Draw a grid
    draw = ImageDraw.Draw(image)

    # Draw grid on x-axis
    y_start = 0
    y_end = image.height


    for x in range(0, image.width, grid_px_size):
        line = ((x, y_start), (x, y_end))
        draw.line(line, grid_color)

    # Draw grid on y-axis
    x_start = 0
    x_end = image.width

    for y in range(0, image.height, grid_px_size):
        line = ((x_start, y), (x_end, y))
        draw.line(line, grid_color)

    # Draw border
    line_top = ((x_start, y_start), (x_end, y_start))
    line_right = ((x_end -1, y_start), (x_end - 1, y_end))
    line_bottom = ((x_start, y_end - 1), (x_end, y_end - 1))
    line_left = ((x_start, y_start), (x_start, y_end))

    draw.line(line_top, border_color)
    draw.line(line_right, border_color)
    draw.line(line_bottom, border_color)
    draw.line(line_left, border_color)

    del draw

    filename = "grid-{}-{}-{}.png".format(width, height, grid_px_size)
    print("Saving {}".format(filename))
    image.save(filename)



    