from PIL import Image
import io,os
ALLOWED_IMAGE_TYPES = ["image/jpeg", "image/png"]
maximum_dimension = 1024
def validate_image(content:bytes,content_type:str) -> dict:
    """Validate the uploaded image content and type."""
    if not content_type.startswith("image/"):
        return False
    if content_type not in ALLOWED_IMAGE_TYPES:
        return False
    
    size_mb = len(content) / (1024 * 1024)

    if size_mb >15:  # Limit to 15 MB
        return 
    image = Image.open(io.BytesIO(content))
    width, height = image.size

    return {
        "is_valid": True,
        "message": "Image is valid.",
        "width": width,
        "height": height,
        "size_mb": size_mb
    }
    # Additional validation logic can be added here (e.g., check image dimensions, format, etc.)

def resize_image(content:bytes) -> bytes:
    """Resize the image to fit within the specified dimensions while maintaining aspect ratio."""
    image = Image.open(io.BytesIO(content))
    width,height = image.size
    if width<=maximum_dimension and height<=maximum_dimension:
        return content  # No resizing needed
    if width>height:
        new_width = maximum_dimension
        new_height = int((maximum_dimension / width) * height)    
    else:
        new_height = maximum_dimension
        new_width = int((maximum_dimension / height) * width)  


    resized_image = image.resize((new_width,new_height), Image.ANTIALIAS)
    output=io.BytesIO()
    resized_image.save(output, format=image.format)
    return output.getvalue()

def save_image(content:bytes, upload_path:str, filename:str)->str:
    """Save the image to disk."""
    os.makedirs(upload_path, exist_ok=True)
    file_path = os.path.join(upload_path, filename)
    with open(file_path, "wb") as f:
        f.write(content)
    return file_path    