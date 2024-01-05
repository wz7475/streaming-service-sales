from typing import Annotated

from fastapi import FastAPI, Depends, HTTPException

from service.dependencies import get_learning_manager, get_experiments_manager
from service.experiments.manager import ExperimentsManager
from service.learning.errors import ArtistNotFound, UnknownModel
from service.learning.manager import LearningManager, EModel

app = FastAPI()


@app.get("/experiments/get")
def get_experiments(limit: int = 1000, artist: str = None,
                    model: EModel = EModel.All):
    pass


@app.get("/predict/info/{artist_id}")
def get_predict_info(artist_id: str):
    pass


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


# OLD
# OLD

# OLD
# OLD
# OLD
# OLD
# OLD
# OLD
# OLD
# OLD
# OLD
# OLD




@app.get("/all")
def prediction(learning_manager: Annotated[
    LearningManager, Depends(get_learning_manager)]):
    models = [learning_manager.get_artist("34")]
    import pickle
    return [(
        model.id,
        pickle.loads(model.naive_model).predict(10, 12)
    ) for model in models]


@app.get("/experiments/all")
def experiments_all(experiments_manager: Annotated[
    ExperimentsManager, Depends(get_experiments_manager)]):
    return experiments_manager.get_all()


@app.get("/predict/{artist_id}/{start}/{periods}")
def predict_random(artist_id: str, start: int, periods: int,
                   experiments_manager: Annotated[
                       ExperimentsManager, Depends(get_experiments_manager)]):
    try:
        return experiments_manager.perform_experiment(artist_id, start,
                                                      periods)
    except ArtistNotFound as ex:
        raise HTTPException(status_code=404, detail=ex.message)
    except UnknownModel as ex:
        raise HTTPException(status_code=400, detail=ex.message)


@app.get("/predict/{artist_id}/{model}/{start}/{periods}")
def predict(artist_id: str, model: EModel, start: int, periods: int,
            learning_manager: Annotated[
                LearningManager, Depends(get_learning_manager)]):
    try:
        return learning_manager.get_prediction(artist_id, model, start,
                                               periods)
    except ArtistNotFound as ex:
        raise HTTPException(status_code=404, detail=ex.message)
    except UnknownModel as ex:
        raise HTTPException(status_code=400, detail=ex.message)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
