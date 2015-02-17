from rq import Queue

from app.helper import count_words_at_url
from worker import conn


q = Queue(connection=conn)
job = q.enqueue_call(func=count_words_at_url, args=('http://www.lorenamesa.com',), result_ttl=5000)