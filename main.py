from flask import Request, Response

# importing the helpers to connect to the database
from helpers import connect


@connect
def entry_point(request: Request = None, conn=None) -> Response:
    '''HTTP Cloud Function.
    Parameters:
        - request (flask.Request): The request object.
        <http://flask.pocoo.org/docs/1.0/api/#flask.Request>
        - conn (psycopg2.connection): The connection passed by the connect decorator
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>.
    '''
    cur = conn.cursor()
    cur.execute("SELECT now()")

    return str(cur.fetchone()[0])
