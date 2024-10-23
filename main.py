from webstorm import Storm, display_html

# Create a Storm object
storm = Storm()

@storm.route('/')
def home():
    return display_html('index.html')

# about page
@storm.route('/about')
def about():
    return display_html('about.html')

# contact page
@storm.route('/contact')
def contact():
    return display_html('contact.html')

# Run the server
storm.start()