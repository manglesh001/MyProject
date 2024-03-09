# Seam-Carving-Algorithm-for-Content-Aware-Image-Resizing


## Description

Seam carving is a content-aware image resizing technique where the image is reduced in size by one pixel of height (or width) at a time. It works by identifying and removing the lowest energy seam from the image.

## What is Seam Carving?

Seam carving is a content-aware image resizing technique where the image is reduced in size by one pixel of height (or width) at a time. It operates by finding the lowest energy seam in the image and removing it.

- A vertical seam is a path of pixels connected from the top to the bottom with one pixel in each row.
- A horizontal seam is a path of pixels connected from the left to the right with one pixel in each column.
- The algorithm consists of three main steps:
  1. Energy Calculation: Calculate the energy for each pixel using an energy function.
  2. Seam Identification: Identify the lowest energy seam in the image.
  3. Seam Removal: Remove the lowest energy seam from the image.

## Output

The generated output images for the sample inputs can be found at `./data/output/sample_out.jpeg`. The RGB values used for generating the output images are stored in `./data/output/rgb_out.txt`.

Here are some visual comparisons between the input and output images:

| Input Image | Output Image |
| :---: | :---: |
| ![Input Image](artifacts/input1.jpeg) | ![Output Image](artifacts/output1.jpeg) |
| ![Input Image](artifacts/input2.jpeg) | ![Output Image](artifacts/output2.jpeg) |
| ![Input Image](artifacts/input3.png) | ![Output Image](artifacts/output3.png) |

## Program Flow

1. Extract individual pixel RGB values from the sample image `./data/input/sample.jpeg` and save them in `./data/input/rgb_in.txt`.
2. Load the RGB values from `./data/input/rgb_in.txt` into a 3D matrix.
3. Implement the seam carving algorithm (inside the `solve()` function in `main.cpp`).
4. Save the individual pixel RGB values for the resized image in `./data/output/rgb_out.txt`.
5. Generate the output sample image `./data/output/sample_out.jpeg` using the RGB values in `./data/output/rgb_out.txt`.

For convenience, a Python script `./src/driver.py` is provided, which performs the first and fifth tasks. The corresponding `./src/main.cpp` file is executed by the Python script to handle the second and fourth tasks.


## File structure

- src/
  - main.cpp
  - driver.py
- data/
  - input/
    - sample1.jpeg
  -output/
    - output.jpeg
- artifacts/
- bin/


## Dependencies:

You'll need to install the Python image library Pillow to extract RGB values of each pixel and to generate images from RGB values.

To install Pillow, run the following command:

```shell
pip install Pillow
```


Please note that the provided Python script is only compatible with Linux/Mac operating systems. If you're a Windows user, you can request the input text file (`rgb_in.txt`) from us to work on the problem.


## How to Run:

1. Open the directory in the terminal.
2. Run the Python script `driver.py` located in `/src`. Pass the input image filename (must be present inside `/data/input`) as a command line argument.

**Ex**:
```bash
python ./src/driver.py sample1.jpeg

```
**Note:** Make sure to have the necessary input image file (`sample1.jpeg` in the above example) in the `/data/input` directory before running the script.

**Note:** Make sure to replace the example image file name (`sample1.jpeg`) with the actual image file you want to use.

## Reference 

The Calculation ofGradient Matrix and details of Seam Carving Algorithm was reffered from an Assignment from Princton University which can be found [here](https://www.cs.princeton.edu/courses/archive/fall17/cos226/assignments/seam/index.html)

## Contributions

Contributions are welcome! If you encounter any issues or have suggestions for improvements, please open an issue or submit a pull request.

