from typing import Annotated

from fastapi import FastAPI, Depends, HTTPException

from service.dependencies import get_learning_manager, get_experiments_manager
from service.experiments.manager import ExperimentsManager
from service.learning.errors import ArtistNotFound, UnknownModel
from service.learning.manager import LearningManager
from service.learning.emodel import EModel

description = """
Forecasting Listening Time

Experiments
- can perform A/B experiment for two models 
- can query experiment result and past predictions

Prediction
- can use naive or complex model to generate predictions
"""

tags_metadata = [
    {
        "name": "Results",
        "description": "View previous prediction results"
    },
    {
        "name": "Experiment",
        "description": "Run predictions (A/B experiment)"
    },
    {
        "name": "Predictions",
        "description": "Run predictions with the selected model"
    }
]

app = FastAPI(
    title="Forecasting Listening Time",
    description=description,
    openapi_tags=tags_metadata
)


@app.get("/experiments/get", tags=["Results"])
def get_experiments(experiments_manager: Annotated[
    ExperimentsManager, Depends(get_experiments_manager)], limit: int = 1000,
                    artist: str = None, model: EModel = EModel.All):
    return experiments_manager.get(limit, artist, model)


@app.get("/experiments/get/all", tags=["Results"])
def get_experiments(experiments_manager: Annotated[
    ExperimentsManager, Depends(get_experiments_manager)]):
    return experiments_manager.get_all()


@app.get("/predict/info/{artist_id}", tags=["Results"])
def get_predict_info(artist_id: str, learning_manager: Annotated[
    LearningManager, Depends(get_learning_manager)]):
    try:
        artist = learning_manager.get_artist(artist_id)
        return [artist.train_begin, artist.train_end]
    except ArtistNotFound as ex:
        raise HTTPException(status_code=404, detail=ex.message)


@app.get("/predict/{artist_id}/{start}/{periods}", tags=["Experiment"])
def get_predict_random(artist_id: str, start: int, periods: int,
                       experiments_manager: Annotated[
                           ExperimentsManager, Depends(
                               get_experiments_manager)]):
    try:
        return experiments_manager.perform_experiment(artist_id, start,
                                                      start + periods)
    except ArtistNotFound as ex:
        raise HTTPException(status_code=404, detail=ex.message)
    except UnknownModel as ex:
        raise HTTPException(status_code=400, detail=ex.message)


@app.get("/predict/{artist_id}/{start}/{periods}/{model}", tags=["Predictions"])
def get_predict_model(artist_id: str, start: int, periods: int, model: EModel,
                      learning_manager: Annotated[
                          LearningManager, Depends(get_learning_manager)]):
    try:
        if model == EModel.All:
            return [
                learning_manager.get_prediction(artist_id, EModel.Naive, start,
                                                start + periods),
                learning_manager.get_prediction(artist_id, EModel.Complex,
                                                start,
                                                start + periods)
            ]

        return learning_manager.get_prediction(artist_id, model, start,
                                               start + periods)
    except ArtistNotFound as ex:
        raise HTTPException(status_code=404, detail=ex.message)
    except UnknownModel as ex:
        raise HTTPException(status_code=400, detail=ex.message)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
