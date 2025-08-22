# PDF-Upscaler

A handy Python tool to upscale any PDF pages (obviously as images!) using Real-ESRGAN.

## Description

This tool takes a PDF file as input, extracts each page as an image, upscales the images using Real-ESRGAN, and then combines the upscaled images back into a PDF file. It uses the Real-ESRGAN ncnn Vulkan executable for upscaling, which is a portable version that doesn't require installing PyTorch or CUDA dependencies.

The tool features progress bars during all stages of processing and provides clear help messages for ease of use.

## Prerequisites

- Python 3.x
- ImageMagick (for creating test images, not required for normal operation)

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/soymh/PDF-Upscaler
   cd PDF-Upscaler
   ```

2. Install the required Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Ensure the Real-ESRGAN executable has proper permissions:
   ```bash
   chmod +x realesrgan-ncnn-vulkan-20220424-ubuntu/realesrgan-ncnn-vulkan
   ```

## Usage

```bash
python pdf_upscaler.py -i input.pdf -o output.pdf
```

### Options

- `-i`, `--input_pdf`: Path to the input PDF file (required)
- `-o`, `--output_pdf`: Path for the output upscaled PDF file (default: upscaled_output.pdf)
- `-n`, `--model_name`: Model name to use for upscaling (default: realesr-animevideov3)
  - Available models: realesr-animevideov3 (default)
- `-s`, `--outscale`: The final upsampling scale of the image (2, 3, or 4) (default: 2)
- `--suffix`: Suffix of the restored image files before merging into PDF (default: upscaled)
- `--fp32`: Use fp32 precision during inference (default: fp16/half precision)

### Examples

```bash
# Basic usage with default settings
python pdf_upscaler.py -i document.pdf -o upscaled_document.pdf

# Using fp32 precision
python pdf_upscaler.py -i document.pdf -o upscaled_document.pdf --fp32
```

### Help

Running the script without arguments or with `-h` or `--help` will display the help message with all available options.

## How it works

1. The tool extracts each page of the PDF as a high-resolution image with progress indication
2. Each image is upscaled using the Real-ESRGAN ncnn Vulkan executable with a real-time progress bar
3. The upscaled images are combined back into a PDF file with a progress bar

## Models

The tool includes the following model:
- realesr-animevideov3 (default): Optimized for anime and cartoon images, works well with most types of images

**Note:** Other models have been removed due to file corruption issues. Only the default model is available.

All models support upscaling factors of 2, 3, and 4. The default upscaling factor is 2.

## Notes

- The Real-ESRGAN executable is portable and includes all binaries and models required
- No CUDA or PyTorch environment is needed
- The upscaling process may take some time depending on the number of pages and the upscale factor
- Higher upscale factors (3x, 4x) will produce larger output files and take more time
- Progress bars are displayed during all stages of processing for better user experience
- Clear error messages and help information are provided for ease of use

## Notes

- The Real-ESRGAN executable is portable and includes all binaries and models required
- No CUDA or PyTorch environment is needed
- The upscaling process may take some time depending on the number of pages and the upscale factor
- Higher upscale factors (3x, 4x) will produce larger output files and take more time
- Progress bars are displayed during all stages of processing for better user experience
- Clear error messages and help information are provided for ease of use
