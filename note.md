#### start with it
- train sarima for individual artists
	- split 80/20 (most 20% of  data for test)
	- fine tune
- compare model performance on other artists

#### accuracy considerations
- multivariate time series (all artists)
- cluster time series - model per cluster
- lstm

#### micro-service coniderations
- model updates
	- retrain model on each data update
	- retrain model periodically 
	- create and train model on each request (per artists / lots of clusters)
- cases like down time for retraining