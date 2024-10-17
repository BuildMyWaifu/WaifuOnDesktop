import uvicorn
from os import getenv
from dotenv import load_dotenv
load_dotenv()


if __name__ == "__main__":
    uvicorn.run(
        app="BMW.__main__:app",
        host="127.0.0.1",
        port=int(getenv("PORT", 8000)),
        reload=True,
    )
