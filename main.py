import os
from dotenv import load_dotenv
from fastmcp import FastMCP
from fastmcp.utilities.types import Image
from mcp.types import Icon

load_dotenv(override=True)

icon_image = Image(path="kaggle.png")

mcp = FastMCP(
    "KaggleDatasets",
    website_url="https://www.kaggle.com",
    icons=[Icon(src=icon_image.to_data_uri())],
)

DOWNLOAD_DIR = os.getenv("DOWNLOAD_DIR", r"E:/kaggle-datasets")


def get_api():
    from kaggle.api.kaggle_api_extended import KaggleApi  # moved here
    api = KaggleApi()
    api.authenticate()
    return api


@mcp.tool()
def search_datasets(query: str, max_results: int = 5) -> list[dict]:
    """Search Kaggle datasets by keyword."""
    api = get_api()
    results = api.dataset_list(search=query)[:max_results]
    return [{"ref": str(d.ref), "title": str(d.title)} for d in results]


@mcp.tool()
def list_dataset_files(dataset: str) -> list[str]:
    """List files in a dataset. Use the format 'owner/dataset-name'."""
    api = get_api()
    files = api.dataset_list_files(dataset).files
    return [f.name for f in files]


@mcp.tool()
def download_dataset(dataset: str) -> dict:
    """Download and unzip a dataset. Use the format 'owner/dataset-name'."""
    api = get_api()
    target = os.path.join(DOWNLOAD_DIR, dataset.replace("/", "_"))
    os.makedirs(target, exist_ok=True)
    api.dataset_download_files(dataset, path=target, unzip=True)
    return {"saved_to": target, "files": os.listdir(target)}


if __name__ == "__main__":
    mcp.run()