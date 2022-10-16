docker stop steamProducer
docker container rm steamProducer
docker build ../python/ --tag tap:python
docker run --network tap -e PYTHON_APP=GetSteamReviews.py --name steamProducer -v $PWD/../.dataset:/usr/src/app/.dataset -it tap:python $1 $2