import uvicorn
import os

# from src.models.enums import EnvEnum

if __name__ == "__main__":
    # if os.getenv("FASTAPI_ENV") == EnvEnum.LOCAL.value:
    uvicorn.run("src.app:app", host="0.0.0.0", port=8023, reload=True, workers=4)
# else:
#     uvicorn.run('src.app:app', host="0.0.0.0",
#                 port=8023, reload=False, workers=4)
