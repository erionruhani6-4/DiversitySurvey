import requests

def generate_image(prompt: str, filename: str = "generated-image.jpg"):
    """
    Sends a request directly to Cloudflare AI API and saves the generated image.
    """
    API_URL = "https://api.cloudflare.com/client/v4/accounts/3b89712328122d1880b1634761a26a5e/ai/run/@cf/bytedance/stable-diffusion-xl-lightning"
    API_TOKEN = "P9YYc-P9eTIE5doqOPFR46Tgfm7iW9m2IjBDbsNS"
    
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {"prompt": prompt}

    response = requests.post(API_URL, json=payload, headers=headers)

    if response.status_code == 200:
        # Save the image
        with open(filename, "wb") as f:
            f.write(response.content)
        print(f"✅ Image saved as {filename}")
    else:
        print(f"❌ Failed to generate image: {response.status_code} - {response.text}")

