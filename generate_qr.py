import qrcode
import json
import os

def generate_qr_code(input_file, output_file):
    """Generate QR code from text or JSON file"""
    
    # Read the input file
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Try to parse as JSON, if it fails, treat as plain text
    try:
        data = json.loads(content)
        qr_data = json.dumps(data, ensure_ascii=False)
    except json.JSONDecodeError:
        qr_data = content
    
    # Create QR code instance
    qr = qrcode.QRCode(
        version=1,  # Controls the size of the QR code
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    
    # Add data to the QR code
    qr.add_data(qr_data)
    qr.make(fit=True)
    
    # Create an image from the QR Code instance
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Save the image
    img.save(output_file)
    print(f"QR code generated successfully and saved to: {output_file}")
    print(f"Data encoded: {qr_data[:100]}..." if len(qr_data) > 100 else f"Data encoded: {qr_data}")

if __name__ == "__main__":
    # Get the directory of the script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Input and output file paths
    input_file = os.path.join(script_dir, "a.txt")
    output_file = os.path.join(script_dir, "qr_code.png")
    
    # Generate QR code
    generate_qr_code(input_file, output_file)
