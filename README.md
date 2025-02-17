# WebStorm Web Framework

WebStorm is a lightweight Python web framework. It provides a simple and intuitive way to create web applications with minimal setup.

## Features

- Simple routing system
- Static file serving
- HTML template rendering
- Easy-to-use decorator-based route definitions

## Installation

You can install WebStorm using pip:

```bash
git clone https://github.com/Shabari-K-S/webstorm.git
cd webstrom
```

create project inside this folder

## Quick Start

Here's a simple example to get you started:

```python
from webstorm import Storm, display_html
app = Storm()

@app.route('/')
def home():
    return display_html('index.html')

@app.route('/about')
def about():
    return display_html('about.html')

if __name__ == '__main__':
    app.start()
```

This will start a web server on `localhost:8080` and serve the static files in the `static` directory.

## Project Structure

A basic WebStorm project structure looks like this:

```text
your_project/
│
├── main.py
├── assets/
│   ├── img/
│   │   └── your_image.png
│   └── css/
│       └── your_styles.css
└── templates/
    ├── index.html
    └── about.html
```

## Serving Static Files

WebStorm automatically serves static files from the `assets` directory. You can reference them in your HTML like this:

```html
<img src="/assets/img/your_image.png" alt="Your Image">
```

## HTML Templates

Place your HTML templates in the `templates` directory. Use the `display_html()` function to render them:

```python
from webstorm import display_html

@app.route('/')
def home():
    return display_html('index.html')
```

## Running Your Application

To run your WebStorm application:

1. Create a Python file (e.g., `main.py`) with your routes and WebStorm setup.
2. Run the file using Python:

```bash
python main.py
```

Your application will start, and you can access it at `http://localhost:8080` by default.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
