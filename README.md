Image Labeling Tool
Overview
The Image Labeling Tool is a Python application designed to allow users to load images from a folder, view them, and create annotations for specific objects within the images. Annotations include points, rectangles, circles, and polygons, each associated with a label. The tool features a user-friendly graphical interface with a dark theme and provides options for zooming, panning, and saving annotations in JSON format.

Features
Folder Selection: Load images from a selected folder. Supports .jpg and .png formats.
Image Viewer: View images in a central display area with automatic fitting to maintain aspect ratio.
Label Management: Add and remove labels for annotating objects within the images.
Annotation Tools: Select tools to draw points, rectangles, circles, and polygons.
Annotation List: View and manage all annotations including label, type, and coordinates.
Save Annotations: Save annotations in a JSON file with the same name as the image.
Dark Theme: Modern dark-themed UI for better usability.
Tool Pane: Tool options located on the right side of the interface.
Installation
Ensure you have Python installed (Python 3.x is recommended).

Install the required packages using pip:

bash
Copy code
pip install pillow
Usage
Run the Application: Execute the Python script to start the application.

bash
Copy code
python image_labeling_tool.py
Open Folder: Use the "File" menu to open a folder containing images.

Select Image: Choose an image from the list to view it in the central image viewer.

Manage Labels: Add or remove labels using the provided text entry and buttons.

Create Annotations: Select a tool from the right-side pane and draw annotations on the image.

View Annotations: Check the list of annotations in the left-side pane.

Save Annotations: Save annotations to a JSON file by selecting "Save Annotations" from the "File" menu.

Tools
Point: Click to place a point annotation.
Rectangle: Click and drag to draw a rectangle annotation.
Circle: Click and drag to draw a circle annotation.
Polygon: Click to create a polygon annotation.
Additional Information
Zooming/Panning: This version does not include zooming/panning functionality. (Feature request can be submitted if needed.)
Dark Theme: The UI is styled with a dark theme for better visibility.
License
This project is licensed under the MIT License. See the LICENSE file for details.

Author
Mudassar Ali

For any issues or feature requests, please contact Mudassar Ali.
