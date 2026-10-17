# Kaggle MCP Server

A small MCP (Model Context Protocol) server that lets Claude **search**, **inspect**, and **download** datasets from Kaggle. You just talk to Claude in plain English, and Claude calls the tools for you.

Built with Python, [FastMCP](https://gofastmcp.com), and the Kaggle API.

---

## What can it do?

| Tool | What it does | Input |
|---|---|---|
| `search_datasets` | Searches Kaggle for datasets by keyword | `query`, optional `max_results` (default 5) |
| `list_dataset_files` | Shows the files inside a dataset | `dataset` as `owner/dataset-name` |
| `download_dataset` | Downloads and unzips a dataset to your computer | `dataset` as `owner/dataset-name` |

Downloaded datasets are saved in their own folder, named `owner_dataset-name`.

**Default download location on Windows:** `C:/Users/<your-username>/kaggle-datasets/`

Example: `C:/Users/<your-username>/kaggle-datasets/uciml_red-wine-quality-cortez-et-al-2009/winequality-red.csv`

You can change the download location by adding `DOWNLOAD_DIR` to your `.env` file. For example, `DOWNLOAD_DIR=D:/kaggle-datasets` saves datasets under `D:/kaggle-datasets/`.

---

## Requirements

- Python 3.11 or newer
- [uv](https://docs.astral.sh/uv/) (a fast Python package manager)
- A free Kaggle account and a Kaggle API token
- [Claude Desktop](https://claude.ai/download) (to use the server from chat)

---

## Setup

### 1. Get your Kaggle API token

1. Log in to [kaggle.com](https://www.kaggle.com).
2. Go to **Settings** and find the **API** section.
3. Create a new token and copy it.

### 2. Install the project

Open a terminal in the cloned repository folder:

```bash
cd Kaggle-MCP-Server
uv add fastmcp kaggle python-dotenv
```

### 3. Add your token

Create a file named `.env` in the project folder:

```env
KAGGLE_API_TOKEN=your_token_here
```

To choose a custom dataset download folder, you can also add this line:

```env
DOWNLOAD_DIR=D:/kaggle-datasets
```

> **Important:** Never share your token or upload `.env` to GitHub. Add `.env` to your `.gitignore` file.

---

## Test it locally (MCP Inspector)

Before connecting to Claude, check that the tools work:

```bash
uv run fastmcp dev inspector main.py
```

This opens MCP Inspector in your browser. Open the **Tools** tab and try each tool:

1. `search_datasets` with a query like `wine quality`
2. `list_dataset_files` with a dataset like `uciml/red-wine-quality-cortez-et-al-2009`
3. `download_dataset` with the same dataset

> If your server file is not called `main.py`, use your file name instead.

---


## Add it to Claude Desktop

You can connect the Kaggle MCP Server to Claude Desktop using either of the following methods.

### Option 1: Install using FastMCP (Recommended)

Run this command from your project folder:

```bash
uv run fastmcp install mcp-json main.py
```

Follow any prompts shown by the command, then restart Claude Desktop if required.

> If your server file is not called `main.py`, replace it with your actual Python file name.

### Option 2: Configure Claude Desktop manually

1. Open Claude Desktop and go to **Settings > Developer > Edit Config**.
2. This opens `claude_desktop_config.json`. Add the following configuration inside the file:

```json
{
  "mcpServers": {
    "KaggleDatasets": {
      "command": "uv",
      "args": [
        "--directory",
        "D:\\path\\to\\Kaggle-MCP-Server",
        "run",
        "main.py"
      ]
    }
  }
}
```

3. Replace `D:\\path\\to\\Kaggle-MCP-Server` with the actual absolute path to your local repository folder.
4. Save the file and **fully restart** Claude Desktop (quit it from the system tray, then open it again).
5. Open a new chat and check that the Kaggle MCP tools are available.

> **Note:** Choose either Option 1 or Option 2. You do not need to use both methods.

---

## How to use it

Just ask Claude. Examples:

- "Search Kaggle for wine quality datasets."
- "Show me the files inside `uciml/red-wine-quality-cortez-et-al-2009`."
- "Download the first Titanic dataset from Kaggle."
- "Search for 5 different datasets on Kaggle and download them."

---

## Rate limits

Kaggle can slow you down (a `429 Too Many Requests` error) if you send too many requests too quickly. Normal use is fine. If you download many datasets in a loop, add a short delay between requests. If you see a 429 error, wait a bit and try again.

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `401 Unauthorized` or authentication error | Your token is wrong or expired. Create a new one and update `.env`. |
| Token not loading | Make sure `.env` is in the project folder and the code loads it before importing Kaggle. |
| Tools don't show up in Claude Desktop | Check the path in `claude_desktop_config.json`, then restart Claude Desktop fully. |
| `429 Too Many Requests` | Wait a few minutes and retry. |
| Download fails or file is missing | Check that you have disk space, Kaggle access, and permission to write to the download folder. If you set `DOWNLOAD_DIR`, confirm that the path is valid. |

---

## Project ideas for later

- Make the server **remote** (HTTP transport) so other people can use it too.
- Add a tool to preview the first rows of a downloaded CSV.

---

## License

This repository includes an MIT license. See [`LICENSE`](LICENSE) for the license text.
