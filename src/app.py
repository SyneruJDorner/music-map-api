import uvicorn
from src.config import network, logger
from src.routes.api import api_router
from src.routes.error import error_router

# The main function of the api module.
# It bundles all the configs, routes and then starts the server.
def app():
    logger.info("Initializing app...")

    app = network.app
    logger.info("Starting server on " + str(network.settings.url))

    app.include_router(api_router)
    app.include_router(error_router)    
    uvicorn.run(app, host=network.settings.address, port=network.settings.port, log_level='debug')
