import argparse
import os
import subprocess
import sys
import fitz # PyMuPDF
import img2pdf

def upscale_image_with_realesrgan(image_path, output_folder, model_name='realesr-animevideov3', outscale=2, suffix='upscaled', fp32=False, page_num=1, total_pages=1):
    """
    Upscales a single image using Real-ESRGAN executable.
    """
    # Path to the RealESRGAN executable
    realesrgan_path = os.path.join(os.path.dirname(__file__), 'realesrgan-ncnn-vulkan-20220424-ubuntu', 'realesrgan-ncnn-vulkan')
    
    # Make sure the executable has proper permissions
    if not os.access(realesrgan_path, os.X_OK):
        try:
            os.chmod(realesrgan_path, 0o755)
        except Exception as e:
            print(f"Warning: Could not set execute permissions on {realesrgan_path}: {e}")
    
    # Prepare output filename
    imgname, _ = os.path.splitext(os.path.basename(image_path))
    
    if suffix == '':
        output_name = f'{imgname}.png'
    else:
        output_name = f'{imgname}_{suffix}.png'
    
    output_path = os.path.join(output_folder, output_name)
    
    # Build command
    cmd = [
        realesrgan_path,
        '-i', image_path,
        '-o', output_path,
        '-n', model_name,
        '-s', str(outscale),
        '-f', 'png'
    ]
    
    # Execute the command
    try:
        print(f'Upscaling page {page_num}/{total_pages} with Real-ESRGAN executable...')
        # Use Popen to capture output in real-time
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
        
        # Print progress in real-time
        progress_prefix = f"  Progress: "
        for line in process.stdout:
            line = line.strip()
            if line and line.endswith('%'):
                # Clear the line and print updated progress
                sys.stdout.write('\r' + progress_prefix + line)
                sys.stdout.flush()
            elif line:
                # Print any other output on a new line
                print(f"\n  {line}")
        
        # Wait for process to complete
        process.wait()
        
        # Complete the progress line
        sys.stdout.write('\r' + progress_prefix + "100.00%" + '\n')
        sys.stdout.flush()
        
        if process.returncode != 0:
            print(f'Error: Real-ESRGAN process exited with code {process.returncode}')
            return None
            
        return output_path
    except Exception as e:
        print(f'Unexpected error upscaling {imgname}: {e}')
        return None

def main():
    parser = argparse.ArgumentParser(description='Upscale PDF pages using Real-ESRGAN.')
    parser.add_argument('-i', '--input_pdf', type=str, required=True, help='Path to the input PDF file.')
    parser.add_argument('-o', '--output_pdf', type=str, default='upscaled_output.pdf', help='Path for the output upscaled PDF file.')
    parser.add_argument(
        '-n',
        '--model_name',
        type=str,
        default='realesr-animevideov3',
        help=('Model names: realesr-animevideov3 (default)'))
    parser.add_argument('-s', '--outscale', type=int, default=2, help='The final upsampling scale of the image (2, 3, or 4)')
    parser.add_argument('--suffix', type=str, default='upscaled', help='Suffix of the restored image files before merging into PDF')
    parser.add_argument(
        '--fp32', action='store_true', help='Use fp32 precision during inference. Default: fp16 (half precision).')
    
    # If no arguments provided, show help
    import sys
    if len(sys.argv) == 1:
        parser.print_help()
        return
    
    args = parser.parse_args()

    if not os.path.exists(args.input_pdf):
        print(f"Error: Input PDF file not found at {args.input_pdf}")
        return

    temp_img_folder = 'temp_pdf_images'
    upscaled_img_folder = 'upscaled_pdf_images'
    os.makedirs(temp_img_folder, exist_ok=True)
    os.makedirs(upscaled_img_folder, exist_ok=True)

    print(f"Extracting pages from {args.input_pdf}...")
    doc = fitz.open(args.input_pdf)
    total_pages = len(doc)
    image_paths = []
    for i, page in enumerate(doc):
        # Show progress
        progress = (i + 1) / total_pages * 100
        print(f"\r  Extracting: {i+1}/{total_pages} ({progress:.1f}%)", end="", flush=True)
        
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # Render at 2x resolution to get high quality
        img_path = os.path.join(temp_img_folder, f"page_{i+1:04d}.png")
        pix.save(img_path)
        image_paths.append(img_path)
    doc.close()
    print(f"\nExtracted {len(image_paths)} pages.")

    upscaled_image_paths = []
    print("Upscaling extracted pages...")
    total_pages = len(image_paths)
    for i, img_path in enumerate(image_paths):
        page_num = i + 1
        upscaled_path = upscale_image_with_realesrgan(
            image_path=img_path,
            output_folder=upscaled_img_folder,
            model_name=args.model_name,
            outscale=args.outscale,
            suffix=args.suffix,
            fp32=args.fp32,
            page_num=page_num,
            total_pages=total_pages
        )
        if upscaled_path:
            upscaled_image_paths.append(upscaled_path)
    print("Finished upscaling pages.")

    if not upscaled_image_paths:
        print("No images were upscaled. Exiting.")
        return

    print(f"Merging upscaled images into {args.output_pdf}...")
    print("  Progress: [", end="", flush=True)
    with open(args.output_pdf, "wb") as f:
        f.write(img2pdf.convert(upscaled_image_paths))
    print("████████████████████] 100%")
    print(f"Successfully created upscaled PDF: {args.output_pdf}")

    # Clean up temporary folders
    print("Cleaning up temporary files...")
    for f in os.listdir(temp_img_folder):
        os.remove(os.path.join(temp_img_folder, f))
    os.rmdir(temp_img_folder)
    for f in os.listdir(upscaled_img_folder):
        os.remove(os.path.join(upscaled_img_folder, f))
    os.rmdir(upscaled_img_folder)
    print("Cleanup complete.")

if __name__ == '__main__':
    main()
