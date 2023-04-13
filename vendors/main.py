from fastapi import FastAPI, responses

from . import auth, core

app = FastAPI()


@app.post("/user/login/")
async def auth_user(auth_data: core.Auth):
    api = auth.GithubAPI(token=auth_data.token)

    try:
        user = api.get_user_data()
    except auth.InvalidCredentials:
        return responses.JSONResponse(
            status_code=400,
            content={
                "code_transaction": "INVALID_CREDENTIALS",
                "message": "Invalid Credentials.",
            },
        )
    except auth.UnableToGetUserData:
        return responses.JSONResponse(
            status_code=400,
            content={
                "code_transaction": "UNABLE_TO_GE_USER_DATA",
                "message": "Unable to get User Data.",
            },
        )
    else:
        return responses.JSONResponse(
            status_code=200,
            content={
                "code_transaction": "OK",
                "user_data": user,
            },
        )


@app.put("/user/update/")
async def update_user(user_update: core.UserUpdate):
    api = auth.GithubAPI(token=user_update.auth.token)
    user_data = user_update.user.dict()
    user_data = dict(
        filter(
            lambda item: item[1] is not None,
            user_data.items(),
        )
    )

    try:
        user = api.edit_user_data(data=user_data)
    except auth.InvalidCredentials:
        return responses.JSONResponse(
            status_code=400,
            content={
                "code_transaction": "INVALID_CREDENTIALS",
                "message": "Invalid Credentials.",
            },
        )
    except auth.UnableToUpdateUserData as e:
        return responses.JSONResponse(
            status_code=400,
            content={
                "code_transaction": "UNABLE_TO_UPDATE_RECORD",
                "message": f"Invalid input data {e}.",
            },
        )
    else:
        return responses.JSONResponse(
            status_code=200,
            content={
                "code_transaction": "OK",
                "user_data": user,
            },
        )
