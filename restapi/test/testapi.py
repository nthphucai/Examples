# import uvicorn
# from fastapi import FastAPI

# app = FastAPI()


# @app.get("/")
# async def root():
#     return {"message": "Hello World"}


# # at last, the bottom of the file/module
# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1")

import requests

result = {
    "task": "simple-question",
    "domain": "english",
    "context": "string",
}

out = requests.post(
    "http://0.0.0.0:5050/v1/from_query",
    # "http://0.0.0.0:5050/v1/from_search",
    json=result,
    headers={"Content-Type": "application/json"},
)
print(out.json())

# out = requests.get('http://127.0.0.1:8000/').json()
# print(out)
