from celery import Celery
from app import config

app = Celery()
app.conf.broker_url = config.REDIS_URI
app.conf.result_backend = config.REDIS_URI


@app.task(name='delete_all_data_in_db_and_fs', queue="dev")
def delete_all_data_in_db_and_fs():
    pass


@app.task(name='image_process', queue="image_process")
def process_image(img_id):
    pass

@app.task(name='slice', queue="slice")
def slice(img_id):
    pass


@app.task(name='deforestation', queue="image_process")
def deforestation(img_id):
    pass
