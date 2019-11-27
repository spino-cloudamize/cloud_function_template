'''
Utility functions to connect to a postgres db from a cloud function
'''
import logging
import os

import psycopg2

LOGGER = logging.getLogger(__name__)
logging.basicConfig(
        format='[%(asctime)s,%(filename)s,%(funcName)s:%(lineno)d,%(levelname)s] - %(message)s',
        level=os.environ.get('LOG_LEVEL', 'WARN'))


def get_conn_details():
    '''Gets the connection details to the database from the
    selected method of secrets.

    Assumes that the developer pass the secret facility type in a env
    variable called SECRET_METHOD with supported types:
    ENV (free but insecure), KMS (cost money), GCS (cost less money)

    - By default we use ENV.
    - We expect at least the following details: DBNAME, USER, PASSWORD, HOST.
    - Additional details are: PORT, SSLMODE, SSLROOTCERT, SSLKEY, SSLCERT.

    Returns:
        dict: dictionary with the connection details.
    '''
    secret_type = os.environ.get('SECRET_METHOD', 'ENV')

    if secret_type == 'ENV':
        return __get_from_env()
    return None


def __get_from_env():
    '''Returns details from env
    '''
    return {
        'dbname': os.environ['DBNAME'],
        'user': os.environ['USER'],
        'password': os.environ['PASSWORD'],
        'host': os.environ['HOST'],
        'port': os.environ.get('PORT', 5432),
        'sslmode': os.environ.get('SSLMODE', None),
        'sslrootcert': os.environ.get('SSLROOTCERT', None),
        'sslkey': os.environ.get('SSLKEY', None),
        'sslcert': os.environ.get('SSLCERT', None)
    }


def connect(_func=None, *, application_name: str = None) -> None:
    '''Decorator that connects to the database
    '''
    def decorator_connection(func, *args, **kwargs):
        def wrapper(*args, **kwargs):
            conn = __connect(application_name=application_name)
            res = func(conn=conn, *args, **kwargs)
            LOGGER.debug('Closing db connection')
            conn.close()
            return res
        return wrapper

    if _func is None:
        return decorator_connection
    return decorator_connection(_func)


def __connect(application_name: str = None) -> object:
    '''Returns a connection to the postgresql database

    Parameters:
        application_name (str): Name of the cloud function (optional).

    Returns:
        connection: psycopg2 connection object
    '''
    c_props = get_conn_details()
    # getting a connection
    conn = psycopg2.connect(
        dbname=c_props['dbname'],
        user=c_props['user'],
        password=c_props['password'],
        host=c_props['host'],
        port=c_props.get('port', 5432),
        sslmode=c_props.get('sslmode', None),
        sslrootcert=c_props.get('sslrootcert', None),
        sslkey=c_props.get('sslkey', None),
        sslcert=c_props.get('sslcert', None),
        application_name=application_name)

    LOGGER.debug("Creating the connection")

    return conn
