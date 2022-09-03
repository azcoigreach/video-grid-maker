'''
Proceedurally create video test patters for LED and Projected video Projects

Tech Stack: Python3 pillow fast-api
'''
from fastapi import FastAPI, Response, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from PIL import Image, ImageDraw, ImageFont
import math

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

#create new function to handle all the parameters. 
# use video-grid-maker.ipynb for reference
@app.get("/grid")
async def grid(width: int = 1920, 
            height: int = 1080, 
            background_color: str = "0, 0, 0, 96", 
            border_color: str = "(0, 255, 0, 255)", 
            border_line_width: int = 2, 
            grid_color: str ="(255, 255, 255, 127)", 
            grid_width: int = 64, 
            grid_height: int = 64, 
            grid_line_width: int = 2, 
            diagnol_color: str = "(255, 72, 26, 255)",
            diagnol_line_width: int = 2,
            circle_color: str = "(255, 72, 26, 255)",
            circle_line_width: int = 2,
            font_size_top: int = 32,
            font_size_bottom: int = 32,
            font_color: str = "(255, 255, 255, 255)",
            font_path: str = "./fonts/Roboto-Regular.ttf",
            text_top: str = "Top Text",
            text_padding_top: int = 15,
            text_padding_bottom: int = 15,
            logo_filename:  str = "./images/SeekPng.com_placeholder-png_3500407.png",
            logo_width: int = 200,
            logo_height: int = 200,
            logo_top: int = 600,
            smpte_color_bar_height: int = 150,
            smpte_color_bar_width: int = 800,
            smpte_color_bar_top: int = 150,
            draw_grid: bool = True, 
            draw_border: bool = True, 
            draw_circle: bool = True, 
            draw_text_top: bool = True, 
            draw_text_bottom: bool = True, 
            draw_diagnol: bool = True, 
            draw_smpte_color_bar: bool = True, 
            draw_logo: bool = True
            ):
    
    # Initiate image
    image = Image.new('RGBA', size=(width, height), color=tuple(map(int, background_color.split(","))))

    # Draw grid on the image using the grid color and grid line width 
    # Do not draw over the border
    if draw_grid:
        draw = ImageDraw.Draw(image)
        for x in range(0, width, grid_width):
            draw.line((x, 0, x, height), fill=grid_color, width=grid_line_width)
        for y in range(0, height, grid_height):
            draw.line((0, y, width, y), fill=grid_color, width=grid_line_width)
        del draw

    
    # Draw a diagnol on the image using the diagnol color and diagnol line width
    if draw_diagnol:
        draw = ImageDraw.Draw(image)
        draw.line((0, 0, width, height), fill=diagnol_color, width=diagnol_line_width)
        draw.line((width, 0, 0, height), fill=diagnol_color, width=diagnol_line_width)
        del draw
        

    # Draw a perfect circle in the absolute center of the image that touches the shortest side of the image
    if draw_circle:
        draw = ImageDraw.Draw(image)
        if width < height:
            radius = math.floor(width / 2) - border_line_width
        else:
            radius = math.floor(height / 2) - border_line_width
        draw.ellipse((width / 2 - radius, height / 2 - radius, width / 2 + radius, height / 2 + radius), outline=circle_color, width=circle_line_width)
        del draw

    # draw 7 blocks of color for each of the main smpte color bar values. 
    # arrange the block in a 1x7 grid.  use smpte_color_bar_width, smpte_color_bar_height and smpte_color_bar_top to determine the size and location of grid. 
    # reference https://en.wikipedia.org/wiki/SMPTE_color_bars#Digital_video
    if draw_smpte_color_bar:
        draw = ImageDraw.Draw(image)
        smpte_color_bar_colors = [(180, 180, 180, 255), (180, 180, 16, 255), (16, 180, 180, 255), (16, 180, 16, 255), (180, 16, 180, 255), (180, 16, 16, 255), (16, 16, 180, 255)]
        smpte_color_bar_left = (width - smpte_color_bar_width) / 2
        smpte_color_block_width = smpte_color_bar_width / 7
        smpte_color_block_height = smpte_color_bar_height
        for i in range(0, 7):
            draw.rectangle((smpte_color_bar_left + i * smpte_color_block_width, smpte_color_bar_top, smpte_color_bar_left + (i + 1) * smpte_color_block_width, smpte_color_bar_top + smpte_color_block_height), fill=smpte_color_bar_colors[i])
        del draw
    
    # draw RGBA logo in the center of the image
    if draw_logo:
        logo = Image.open(logo_filename)
        # make logo transparent
        logo = logo.convert('RGBA')
        logo = logo.resize((logo_width, logo_height), Image.ANTIALIAS)
        # paste logo on the image with logo_top
        image.paste(logo, (int(width / 2 - logo_width / 2), logo_top), logo)
        del logo    

    # Draw the text variable near the top of the image using font, font_size, font_color, text_padding
    if draw_text_top:
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(font_path, font_size_top)
        text_width, text_height = font.getsize(text_top)
        draw.text(((width - text_width) / 2, text_padding_top), text_top, font=font, fill=font_color)
        del draw

    # draw a line of text at the bottom of the image using font, font_size, font_color, text_padding_bottom
    if draw_text_bottom:
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(font_path, font_size_bottom)
        # draw image size and aspect ratio and grid size as text_bottom
        if draw_grid:
            text_bottom = 'size: %d x %d, ar: %.2f, grid: %d x %d' % (width, height, width / height, grid_width, grid_height)
        else:
            text_bottom = 'size: %d x %d, ar: %.2f' % (width, height, width / height)
        text_width, text_height = font.getsize(text_bottom)
        # center the text at the bottom of the image using text_padding_bottom from the bottom of the text
        draw.text(((width - text_width) / 2, height - text_padding_bottom - text_height), text_bottom, font=font, fill=font_color)
            
        del draw

    # Draw a border on the image using the border color and border line width
    # Keep the border on the image
    if draw_border:
        draw = ImageDraw.Draw(image)
        draw.rectangle((0, 0, width-1, height-1), outline=border_color, width=border_line_width)
        del draw


    # Save the image
    text_top = text_top.replace(' ', '-')
    filename = "grid-{}-{}-{}.png".format(width, height, text_top)
    print("Saving {}".format(filename))
    image.save(filename)