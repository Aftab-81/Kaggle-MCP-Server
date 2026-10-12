import asyncio
from fastmcp import Client
import main


async def run():
    async with Client(main.mcp) as client:
        result = await client.call_tool(
            "download_dataset",
            {"dataset": "ulrikthygepedersen/co2-emissions-by-country"},
        )
        print(result)


asyncio.run(run())