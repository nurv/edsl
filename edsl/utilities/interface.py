from html import escape
from IPython.display import HTML
from IPython.display import display as ipython_diplay
from PIL import Image, ImageDraw, ImageFont
from rich.console import Console
from rich.table import Table


def heartbeat_generator():
    while True:
        for c in "|/-\\":
            yield c


def gen_html_sandwich(html_inner, interactive=False):
    if interactive:
        html_header = """
            <html>
            <head>
            <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.7.1/jquery.min.js"></script>
            <link rel="stylesheet" href="https://cdn.datatables.net/1.13.6/css/jquery.dataTables.css" />
            <script src="https://cdn.datatables.net/1.13.6/js/jquery.dataTables.js"></script>
            <style>
                table {
                    font-family: Arial, sans-serif;
                    border-collapse: collapse;
                    width: 100%;
                }
                
                td, th {
                    border: 1px solid #dddddd;
                    text-align: left;
                    padding: 8px;
                }
                
                tr:nth-child(even) {
                    background-color: #dddddd;
                }
            </style>
            <script>
            $(document).ready( function () {
                $('#myTable').DataTable();
            } )
            </script>
            </head>
            <body>
        """
    else:
        html_header = """
            <html>
            <head>
            <style>
                table {
                    font-family: Arial, sans-serif;
                    border-collapse: collapse;
                    width: 100%;
                }
                
                td, th {
                    border: 1px solid #dddddd;
                    text-align: left;
                    padding: 8px;
                }
                
                tr:nth-child(even) {
                    background-color: #dddddd;
                }
            </style>
            </head>
            <body>
        """

    html_footer = """
        </body>
        </html>
    """
    return html_header + html_inner + html_footer


def view_html(html):
    import tempfile
    import webbrowser

    with tempfile.NamedTemporaryFile("w", delete=False, suffix=".html") as f:
        url = "file://" + f.name
        # Write the HTML content to the file
        f.write(html)

    # Open the URL in the web browser
    webbrowser.open(url)


def human_readable_labeler_creator():
    """Creates a function that maps thread ids to human-readable labels.
    It is structured as a closure, so that the mapping is persistent.
    I.e., when the returned function is called, it will use the same
    dictionary to map thread ids to human-readable labels if it's seen that ID
    before; otherwise, it will add a new entry to the dictionary.
    This will persist across calls to the function.
    """
    d = {}

    def func(thread_id):
        if thread_id in d:
            return d[thread_id]
        else:
            d[thread_id] = len(d)
            return d[thread_id]

    return func


def get_multiline_textsize(text, font):
    # Split the text by lines
    lines = text.split("\n")

    # Initialize width and height
    max_width = 0
    total_height = 0

    for line in lines:
        # Get the size of the text for the line
        box = font.getbbox(line)
        width, height = box[2], box[3]

        # Update max_width if width of the current line is greater than max_width
        max_width = max(max_width, width)

        # Add height to total_height
        total_height += height

    return max_width, total_height


def create_image(console, image_filename):
    font_size = 15

    text = console.export_text()  # Get the console output as text.

    # Create an image from the text
    font_size = 15
    font = ImageFont.load_default()  # Use the default font to avoid file path issues.
    # text_width, text_height = ImageDraw.Draw(
    #    Image.new("RGB", (100, 100))
    # ).multiline_textsize(text, font=font)
    text_width, text_height = get_multiline_textsize(text, font)
    image = Image.new(
        "RGB", (text_width + 20, text_height + 20), color=(255, 255, 255)
    )  # Add some padding
    d = ImageDraw.Draw(image)

    # Draw text to image
    d.multiline_text((10, 10), text, font=font, fill=(0, 0, 0))
    # Save the image
    image.save(image_filename)


def display(console, table, filename):
    if filename is not None:
        with open(filename, "w") as f:
            with console.capture() as capture:
                console.print(table)
            f.write(capture.get())
        create_image(console, filename + ".png")
    else:
        console.print(table)


def print_dict_with_rich(d, key_name="Key", value_name="Value", filename=None):
    console = Console(record=True)
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column(key_name, style="dim")
    table.add_column(value_name, style="dim")
    for key, value in d.items():
        table.add_row(key, str(value))
    display(console, table, filename)


def print_dict_as_html_table(
    d, show=False, key_name="Key", value_name="Value", filename=None
):
    # Start the HTML table
    html_table = f'<table border="1">\n<tr><th>{escape(key_name)}</th><th>{escape(value_name)}</th></tr>\n'

    # Add rows to the HTML table
    for key, value in d.items():
        html_table += (
            f"<tr><td>{escape(str(key))}</td><td>{escape(str(value))}</td></tr>\n"
        )

    # Close the HTML table
    html_table += "</table>"

    # Print the HTML table to console
    # print(html_table)

    # Write to file if a filename is provided
    if filename:
        with open(filename, "w") as file:
            file.write(html_table)
    else:
        if show:
            view_html(gen_html_sandwich(html_table))
        else:
            return html_table


def print_list_of_dicts_with_rich(data, filename=None, split_at_dot=True):
    # Initialize console object
    console = Console(record=True)

    # Create a table object
    table = Table(show_header=True, header_style="bold magenta", show_lines=True)

    # Adding columns to the table
    for d in data:
        for key in d.keys():
            if split_at_dot:
                value = key.replace(".", "\n.")
            else:
                value = key
            table.add_column(value, style="dim")

    # Adding rows to the table
    num_rows = len(next(iter(data[0].values())))
    for i in range(num_rows):
        row = [str(d[key][i]) for d in data for key in d.keys()]
        table.add_row(*row)

    display(console, table, filename)


def print_list_of_dicts_as_html_table(data, filename=None, interactive=False):
    # Start the HTML table

    html_table = '<table id="myTable" class="display">\n'
    html_table += "  <thead>\n"
    # Add the header row
    headers = [key for d in data for key in d.keys()]
    html_table += "  <tr>\n"
    for header in headers:
        html_table += f"    <th>{header}</th>\n"
    html_table += "  </tr>\n"
    html_table += "  </thead>\n</tbody>\n"

    # Determine the number of rows
    num_rows = max(len(values) for d in data for values in d.values())

    # Add the data rows
    for i in range(num_rows):
        html_table += "  <tr>\n"
        for d in data:
            for key in d.keys():
                value = d[key][i] if i < len(d[key]) else ""
                html_table += f"    <td>{value}</td>\n"
        html_table += "  </tr>\n"

    # Close the table
    html_table += "</tbody>\n"
    html_table += "</table>"

    html = gen_html_sandwich(html_table, interactive=interactive)

    # Output or save to file
    if filename:
        with open(filename, "w") as f:
            f.write(html)
    else:
        # view_html(html)
        ipython_diplay(HTML(html))


def print_table_with_rich(data, filename=None):
    # Initialize a console object - expects a list of dictionaries
    console = Console(record=True)

    # Create a new table
    table = Table(show_header=True, header_style="bold magenta", row_styles=["", "dim"])

    # Check if data is empty; if it is, exit
    if not data:
        console.print("No data provided!")
        return

    # Add columns based on keys in the first dictionary
    for key in data[0].keys():
        table.add_column(key, style="dim")

    # Add rows to the table
    for row in data:
        table.add_row(*[str(value) for value in row.values()])

    display(console, table, filename)