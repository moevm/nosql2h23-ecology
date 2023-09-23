from app import app
from app.db import local


@app.task(name='delete_all_data_in_db_and_fs', queue="dev")
def delete_all_data_in_db_and_fs():
    local.db.client.drop_database('ecologyDB')
    print('All database data deleted.')

