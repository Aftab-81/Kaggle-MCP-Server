import os
import re
from pathlib import Path

from dotenv import load_dotenv
from fastmcp import FastMCP
from fastmcp.utilities.types import Image
from mcp.types import Icon

# Folder where this file lives. Using it means the .env and the icon are found
# even if the app starts the server from a different folder.
BASE_DIR = Path(__file__).resolve().parent

# Load the user's own Kaggle token from their .env file (never hard-code it).
load_dotenv(BASE_DIR / ".env", override=True)

icon_image = Image(path=str(BASE_DIR / "kaggle.png"))

mcp = FastMCP(
    "KaggleDatasets",
    website_url="https://www.kaggle.com",
    icons=[Icon(src=icon_image.to_data_uri())],
)

# Where downloads are saved. Users can change it with DOWNLOAD_DIR in their .env.
# Default: a "kaggle-datasets" folder inside the user's home folder (works on any PC).
DOWNLOAD_DIR = os.path.expanduser(
    os.getenv("DOWNLOAD_DIR", os.path.join("~", "kaggle-datasets"))
)

# A Kaggle dataset name looks like "owner/dataset-name".
DATASET_PATTERN = re.compile(r"^[\w.-]+/[\w.-]+$")


def check_dataset_name(dataset: str) -> str:
    """Make sure the dataset name is in the 'owner/dataset-name' format."""
    dataset = dataset.strip()
    if not DATASET_PATTERN.match(dataset):
        raise ValueError(
            "Dataset must be in the format 'owner/dataset-name', "
            "for example 'rohanrao/air-quality-data-in-india'."
        )
    return dataset


def get_api():
    from kaggle.api.kaggle_api_extended import KaggleApi  # imported here so .env loads first

    api = KaggleApi()
    try:
        api.authenticate()
    except Exception:
        # Do not print the original error, so a token can never leak into the chat.
        raise RuntimeError(
            "Kaggle login failed. Check that KAGGLE_API_TOKEN is set correctly "
            "in your .env file (or MCP config), then restart the app."
        ) from None
    return api


@mcp.tool()
def search_datasets(query: str, max_results: int = 5) -> list[dict]:
    """Search Kaggle datasets by keyword."""
    max_results = max(1, min(max_results, 20))  # keep it between 1 and 20
    api = get_api()
    results = api.dataset_list(search=query)[:max_results]
    return [{"ref": str(d.ref), "title": str(d.title)} for d in results]


@mcp.tool()
def list_dataset_files(dataset: str) -> list[str]:
    """List files in a dataset. Use the format 'owner/dataset-name'."""
    dataset = check_dataset_name(dataset)
    api = get_api()
    files = api.dataset_list_files(dataset).files
    return [f.name for f in files]


@mcp.tool()
def download_dataset(dataset: str) -> dict:
    """Download and unzip a dataset. Use the format 'owner/dataset-name'."""
    dataset = check_dataset_name(dataset)
    api = get_api()
    target = os.path.join(DOWNLOAD_DIR, dataset.replace("/", "_"))
    os.makedirs(target, exist_ok=True)
    api.dataset_download_files(dataset, path=target, unzip=True)
    return {"saved_to": target, "files": os.listdir(target)}


if __name__ == "__main__":
    mcp.run()