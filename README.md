# Python Barcode Scanner

## Description
This project implements a barcode scanner using Python. It leverages a webcam to detect barcodes in real-time, fetches product details through an API (in this case, UPCItemDB), and saves the gathered information into an Excel file. It's useful for inventory management or any application requiring quick identification and cataloging of products via barcodes.

## Prerequisites
To run this script, you need to have Python 3.x installed along with the following libraries:
- OpenCV (`cv2`)
- Pyzbar
- Requests
- Pandas

Additionally, you'll need access to a webcam for reading barcodes and an internet connection to make queries to the UPCItemDB API.

## Installation
First, ensure Python is installed on your system. Then, install the necessary dependencies by running the following command in your terminal:

```bash
pip install opencv-python-headless pyzbar requests pandas
```

## Execution
To start the barcode scanner, navigate to the directory where you saved the script and run the following command in your terminal:

```bash
python BarcodeShoeSearch.py
```

## Usage
- Run the script as indicated in the above section.
- Place a barcode in front of the webcam. The script will automatically detect the barcode and display a "Estabilizando..." message before processing the code to avoid misreads.
- Once stabilized and processed, the detected barcode will be looked up in the UPCItemDB database for product information.
- The detected product's details will be added to a list, and upon terminating the script execution (by pressing 'q' to close the scanner window), an Excel file with the collected information will be saved in the current directory.

## Output Example
The generated Excel file will contain columns for Barcode, Product, Brand, Model, Color, Size, Gender, Category, and Product Image URL.
