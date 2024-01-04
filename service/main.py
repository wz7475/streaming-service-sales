from typing import Annotated

from fastapi import FastAPI, Depends, HTTPException

from service.dependencies import get_learning_manager
from service.learning.errors import ArtistNotFound, UnknownModel
from service.learning.manager import LearningManager, EModel

app = FastAPI()


@app.get("/")
def prediction(learning_manager: Annotated[
    LearningManager, Depends(get_learning_manager)]):
    learning_manager.fill()
    return 'filled'


@app.get("/all")
def prediction(learning_manager: Annotated[
    LearningManager, Depends(get_learning_manager)]):
    models = [learning_manager.get_artist("34")]
    import pickle
    return [(
        model.id,
        pickle.loads(model.naive_model).predict(10, 12)
    ) for model in models]


@app.get("/predict/{artist_id}/{model}/{start}/{periods}")
def predict(artist_id: str, model: EModel, start: int, periods: int,
            learning_manager: Annotated[LearningManager, Depends()]):
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
