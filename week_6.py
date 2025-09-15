import requests
import os
import hashlib
from urllib.parse import urlparse
import mimetypes

def create_directory():
    """Create the Fetched_Images directory if it doesn't exist"""
    os.makedirs("Fetched_Images", exist_ok=True)
    print("✓ Fetched_Images directory ready")

def extract_filename(url, content_type=None):
    """Extract filename from URL or generate one based on content type"""
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)
    
    # If no filename in URL, generate one
    if not filename or '.' not in filename:
        # Determine extension from content type or default to jpg
        extension = "jpg"  # default
        if content_type:
            ext = mimetypes.guess_extension(content_type)
            if ext:
                extension = ext.lstrip('.')
        filename = f"downloaded_image.{extension}"
    
    return filename

def is_duplicate_image(content, directory="Fetched_Images"):
    """Check if an image with the same content already exists"""
    # Generate a hash of the image content
    content_hash = hashlib.md5(content).hexdigest()
    
    # Check all files in directory for matching hash
    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)
        if os.path.isfile(file_path):
            with open(file_path, 'rb') as f:
                file_hash = hashlib.md5(f.read()).hexdigest()
                if file_hash == content_hash:
                    return True, file
    
    return False, None

def validate_response(response):
    """Validate the HTTP response before downloading content"""
    # Check status code
    if response.status_code != 200:
        raise requests.exceptions.HTTPError(f"Server returned status code: {response.status_code}")
    
    # Check content type to ensure it's an image
    content_type = response.headers.get('content-type', '')
    if not content_type.startswith('image/'):
        raise ValueError(f"URL does not point to an image (Content-Type: {content_type})")
    
    # Check content length to avoid excessively large files
    content_length = response.headers.get('content-length')
    if content_length and int(content_length) > 10 * 1024 * 1024:  # 10MB limit
        raise ValueError("File size exceeds 10MB limit")
    
    return content_type

def download_image(url, timeout=10):
    """Download an image from a URL with safety checks"""
    print(f"\nAttempting to fetch: {url}")
    
    # Set a user-agent header to identify ourselves
    headers = {
        'User-Agent': 'UbuntuImageFetcher/1.0 (Community Image Collection Tool)'
    }
    
    try:
        # Make HEAD request first to check resource without downloading
        head_response = requests.head(url, headers=headers, timeout=timeout, allow_redirects=True)
        head_response.raise_for_status()
        
        # Get final URL after redirects
        final_url = head_response.url
        print(f"✓ Resource found at: {final_url}")
        
        # Now make the actual GET request
        response = requests.get(final_url, headers=headers, timeout=timeout, stream=True)
        response.raise_for_status()
        
        # Validate response headers
        content_type = validate_response(response)
        
        # Get image content
        image_content = response.content
        
        # Check for duplicates
        is_duplicate, existing_file = is_duplicate_image(image_content)
        if is_duplicate:
            print(f"✓ Image already exists as: {existing_file} (skipping download)")
            return False, existing_file
        
        # Extract filename
        filename = extract_filename(final_url, content_type)
        filepath = os.path.join("Fetched_Images", filename)
        
        # Ensure unique filename if file already exists
        counter = 1
        base, ext = os.path.splitext(filename)
        while os.path.exists(filepath):
            filename = f"{base}_{counter}{ext}"
            filepath = os.path.join("Fetched_Images", filename)
            counter += 1
        
        # Save the image
        with open(filepath, 'wb') as f:
            f.write(image_content)
        
        print(f"✓ Successfully fetched: {filename}")
        return True, filename
        
    except requests.exceptions.RequestException as e:
        print(f"✗ Connection error: {e}")
        return False, None
    except Exception as e:
        print(f"✗ An error occurred: {e}")
        return False, None

def main():
    print("=" * 50)
    print("Welcome to the Ubuntu Image Fetcher")
    print("A tool for mindfully collecting images from the web")
    print("=" * 50)
    
    # Create directory
    create_directory()
    
    # Get URLs from user
    urls_input = input("\nPlease enter image URLs (separate multiple URLs with commas): ")
    urls = [url.strip() for url in urls_input.split(',') if url.strip()]
    
    if not urls:
        print("No URLs provided. Exiting.")
        return
    
    successful_downloads = 0
    total_urls = len(urls)
    
    for url in urls:
        success, filename = download_image(url)
        if success:
            successful_downloads += 1
    
    # Summary
    print("\n" + "=" * 50)
    print("Download Summary:")
    print(f"Attempted: {total_urls}")
    print(f"Successful: {successful_downloads}")
    print(f"Skipped (duplicates/errors): {total_urls - successful_downloads}")
    
    if successful_downloads > 0:
        print("\nConnection strengthened. Community enriched.")
    print("=" * 50)

if __name__ == "__main__":
    main()