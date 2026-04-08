from huggingface_hub import HfApi
import os

token = os.getenv("HF_TOKEN")
repo_id = "Raunakiitp/focusflow_env"

api = HfApi(token=token)

print(f"Creating Hugging Face Space: {repo_id}")
# Create the Space (will do nothing if it already exists)
api.create_repo(
    repo_id=repo_id, 
    repo_type="space", 
    space_sdk="docker", 
    exist_ok=True
)

print("Uploading files to the Hugging Face Docker Space...")
# Upload all current files except pycache and deployment script itself
api.upload_folder(
    folder_path=".",
    repo_id=repo_id,
    repo_type="space",
    ignore_patterns=["__pycache__/*", "*.pyc", "deploy_hf.py", ".git/*"]
)

print(f"Successfully deployed! You can view the build process and your Space at:")
print(f"https://huggingface.co/spaces/{repo_id}")
