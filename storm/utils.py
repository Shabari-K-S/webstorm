import os

def display_html(filename, template_dir='templates'):
    file_path = os.path.join(template_dir, filename)
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return f.read()
    else:
        return f"<h1>404 Not Found</h1><p>Template {filename} does not exist.</p>"
