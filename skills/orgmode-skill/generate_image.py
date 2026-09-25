# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "click",
#     "huggingface-hub",
#     "pillow",
# ]
# ///



import click
import os
import re
from huggingface_hub import InferenceClient
from PIL import Image


def get_api_key():
    """Read API key from ~/.open_hugging_face.token"""
    token_path = os.path.expanduser("~/.open_hugging_face.token")
    if not os.path.exists(token_path):
        raise click.ClickException(
            f"API token file not found: {token_path}\n"
            "Create it with: echo 'your_hf_token' > ~/.open_hugging_face.token"
        )
    with open(token_path) as f:
        key = f.read().strip()
    if not key:
        raise click.ClickException(f"API token file is empty: {token_path}")
    return key


@click.command()
@click.argument("prompt")
@click.option("--model", default="black-forest-labs/FLUX.1-schnell",
              help="Model ID to use")
@click.option("--provider", default="auto",
              help="Inference provider to use (auto, fal-ai, replicate, etc.)")
def main(prompt, model, provider):
    """Generate images from text prompts using HuggingFace models."""
    api_key = get_api_key()
    client = InferenceClient(api_key=api_key, provider=provider)

    image = client.text_to_image(prompt, model=model)

    safe_name = re.sub(r'[^a-zA-Z0-9]', '_', prompt[:30])
    output_file = f"{safe_name}.png"
    image.save(output_file)

    click.echo(f"Image saved to: {output_file}")


if __name__ == "__main__":
    main()
