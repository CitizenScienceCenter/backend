from pony_up.do_update import do_all_migrations
from pony import orm
import os
from dotenv import load_dotenv

def bind_to_database(db):
    load_dotenv()
    db.bind("postgres", user=os.getenv("PG_USER"), port=os.getenv("PG_PORT"), password=os.getenv("PG_PASSWORD"), hostaddr=os.getenv("PG_HOST"), database=os.getenv("PG_DB"))
    db.generate_mapping(create_tables=False)


migrations_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), "migrations")

python_import = "migrations" 
orm.debug = True
try:
    db = do_all_migrations(bind_to_database, folder_path=migrations_folder, python_import=python_import)
except Exception as e:
    from time import sleep
    sleep(2)  # to have some time between logging it and crashing.
    raise e