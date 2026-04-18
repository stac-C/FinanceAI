from vercel_wsgi import make_handler
from FinanceAI.wsgi import application

handler = make_handler(application)