# Video Grid Maker
Proceedurally create video test grids for LED and Projected video projects

## Usage

`uvicorn api.main:app --host 0.0.0.0 --port 8080 --reload`

## Installation
Recommend using Python3 virtual environment.

`python -m venv venv`

`source venv/bin/activate` activate virtual environment in linux

or run `venv/Scripts/Activate.ps1` from inside VS Code activate virtual environment in windows

`pip install -r requirements.txt`

## Features
- Adjust the size and location of most of the elements in the test pattern
- RGBA color selection for each element in the test pattern
- Include Logo
- Custom Text

## TODO
- Show over production and processing segments
- Add background image
- Add different types of test patterns
- create animated test patterns and torture tests
- create FastAPI interface and Dockerize
- add Stranger Production logo as default logo
- add default values for all variables that are dynamic based on image size
