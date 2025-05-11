import requests

def generate_image(prompt: str, filename: str = "generated-image.jpg"):
    """
    Sends a request directly to Cloudflare AI API and saves the generated image.
    """
    API_URL = "https://api.cloudflare.com/client/v4/accounts/{INSERT ACCOUNT NUMBER}/ai/run/@cf/bytedance/stable-diffusion-xl-lightning" # Account number attained at the browser when navigated to the "Account Home Page" #
    API_TOKEN = "insert cloudflare api token"
    
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

