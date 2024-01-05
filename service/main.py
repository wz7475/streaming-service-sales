from typing import Annotated

from fastapi import FastAPI, Depends, HTTPException

from service.dependencies import get_learning_manager, get_experiments_manager
from service.experiments.manager import ExperimentsManager
from service.learning.errors import ArtistNotFound, UnknownModel
from service.learning.manager import LearningManager
from service.learning.emodel import EModel

app = FastAPI()


@app.get("/experiments/get")
def get_experiments(experiments_manager: Annotated[
    ExperimentsManager, Depends(get_experiments_manager)], limit: int = 1000,
                    artist: str = None, model: EModel = EModel.All):
    return experiments_manager.get(limit, artist, model)


@app.get("/experiments/get/all")
def get_experiments(experiments_manager: Annotated[
        ExperimentsManager, Depends(get_experiments_manager)]):
    return experiments_manager.get_all()


@app.get("/predict/info/{artist_id}")
def get_predict_info(artist_id: str, learning_manager: Annotated[
        LearningManager, Depends(get_learning_manager)]):
    try:
        artist = learning_manager.get_artist(artist_id)
        return [artist.train_begin, artist.train_end]
    except ArtistNotFound as ex:
        raise HTTPException(status_code=404, detail=ex.message)


@app.get("/predict/{artist_id}/{start}/{periods}")
def get_predict_random(artist_id: str, start: int, periods: int,
                       experiments_manager: Annotated[
                           ExperimentsManager, Depends(
                               get_experiments_manager)]):
    try:
        return experiments_manager.perform_experiment(artist_id, start,
                                                      periods)
    except ArtistNotFound as ex:
        raise HTTPException(status_code=404, detail=ex.message)
    except UnknownModel as ex:
        raise HTTPException(status_code=400, detail=ex.message)


@app.get("/predict/{artist_id}/{start}/{periods}/{model}")
def get_predict_model(artist_id: str, start: int, periods: int, model: EModel,
                      learning_manager: Annotated[
                          LearningManager, Depends(get_learning_manager)]):
    try:
        if model == EModel.All:
            return [
                learning_manager.get_prediction(artist_id, EModel.Naive, start,
                                                periods),
                learning_manager.get_prediction(artist_id, EModel.Complex,
                                                start,
                                                periods)
            ]

        return learning_manager.get_prediction(artist_id, model, start,
                                               periods)
    except ArtistNotFound as ex:
        raise HTTPException(status_code=404, detail=ex.message)
    except UnknownModel as ex:
        raise HTTPException(status_code=400, detail=ex.message)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
