import os, sys, argparse, logging, atexit, datetime
from pydantic import BaseSettings
from dotenv import load_dotenv
from typing import Optional

# Configure the logging
if os.path.exists("./logs") is False:
    os.mkdir("./logs")

logger = logging.getLogger(__name__)
now = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
log_file_name = f'app_{now}.log'
logging.basicConfig(filename=os.path.join('.', 'logs', log_file_name), level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


'''
Can write to the file using the following commands:
    - logger.debug('This is a debug message')
    - logger.info('This is an info message')
    - logger.warning('This is a warning message')
    - logger.error('This is an error message')
    - logger.critical('This is a critical message')
'''

# Register an app exit handler
def exit_handler():
    logger.info('Shut down - music-map api.')

atexit.register(exit_handler)

class EnvironmentConfig():
    #Check if prod.env exists, if not, load dev.env
    if os.path.exists("prod.env"):
        load_dotenv("prod.env")
    else:#elif os.path.exists("dev.env"):
        load_dotenv("dev.env")

    class Settings(BaseSettings):
        FAST_API_SECRET_KEY: Optional[str]

    class Config():
        # `prod.env` takes priority over `dev.env`
        env_file = "dev.env"
        case_sensitive = True

    settings = Settings()

    if settings.FAST_API_SECRET_KEY is None:
        settings.FAST_API_SECRET_KEY = os.getenv("FAST_API_SECRET_KEY")

class VirtualEnvironmentConfigConfig():
    @classmethod
    def __get_base_prefix_compat(cls):
        """Get base/real prefix, or sys.prefix if there is none."""
        return getattr(sys, "base_prefix", None) or getattr(sys, "real_prefix", None) or sys.prefix

    @classmethod
    def is_within_container(cls):
        # checks for an environement variable to see if the application is running inside a docker container
        # to take advantage of this, we need to add the following line to the dockerfile:
        # ENV WITHIN_DOCKER_CONTAINER True
        WITHIN_DOCKER_CONTAINER = bool(os.environ.get('WITHIN_DOCKER_CONTAINER', False))

        # In order to run the application in github actions, we need to add the following line to the workflow file:
        # This is set from pytest files
        WITHIN_GITHUB_ACTIONS = bool(os.environ.get('GITHUB_ACTIONS', False))
        return WITHIN_DOCKER_CONTAINER or WITHIN_GITHUB_ACTIONS

    @classmethod
    def ensure_virtualenv(cls):
        if cls.is_within_container() is True:
            return

        if not cls.__get_base_prefix_compat() != sys.prefix:
            msg = "Please activate the virtual environment before running the application\n"
            msg += "To create the virtual environment, run the following command (without quotes):\n"
            msg += "    - 'python -m venv venv'\n"
            msg += "To activate the virtual environment, run the following command (without quotes):\n"
            msg += "    - 'venv\\Scripts\\activate'\n"
            print(msg)
            sys.exit(0)

class ArgConfig():
    @classmethod
    def args(cls):
        # Check if running in a test context
        if "pytest" in sys.modules:
            return "api"
        
        #Handle the parameters for the application
        parser = argparse.ArgumentParser(prog = 'python statemachine api', description = 'A statemachine hosted in FastAPI', add_help=False)
        parser.add_argument('-help', '--help', action='store_true', default=False)
        parser.add_argument('-api', '--api', action='store_true', default=False)
        listed_arguments = parser.parse_args()
        
        args = []
        for argument in vars(listed_arguments):
            if getattr(listed_arguments, argument):
                args.append(argument)

        if (len(args) >= 2):
            print("Too many arguments, please use only one argument at a time")
            sys.exit(0)

        if (len(args) == 0):
            print("No argument provided, please use -help to see the list of available arguments")
            sys.exit(0)

        exec_mudule = str(args[0]).lower()
        return exec_mudule

class NetworkConfig():
    try:
        from fastapi import FastAPI
        from fastapi.middleware.cors import CORSMiddleware
        from fastapi.middleware.gzip import GZipMiddleware
        from starlette.middleware.sessions import SessionMiddleware
    
        from slowapi import Limiter, _rate_limit_exceeded_handler
        from slowapi.util import get_remote_address
        from slowapi.errors import RateLimitExceeded
        from slowapi.middleware import SlowAPIMiddleware

        class Settings(BaseSettings):
            app_name = "Music-Map API"
            items_per_user: int = 50
            web_scheme: str = "http"
            address: str = "0.0.0.0" if VirtualEnvironmentConfigConfig.is_within_container() else "localhost"
            port: int = 7000 if VirtualEnvironmentConfigConfig.is_within_container() else 7000
            url = f"{address}:{port}"
            web_url = f"{web_scheme}://{address}:{port}"
        
        settings = Settings()
        app = FastAPI(title=settings.app_name)

        # FAST_API_SECRET_KEY Generated with:
        # import secrets
        # secrets.token_hex(16)
        env = EnvironmentConfig()
        app.add_middleware(SessionMiddleware, secret_key=env.settings.FAST_API_SECRET_KEY)
        ALLOWED_HOSTS = ["*"]
        app.add_middleware(CORSMiddleware, allow_origins=ALLOWED_HOSTS, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
        app.add_middleware(GZipMiddleware, minimum_size=1000)

        base_path = os.path.dirname(os.path.realpath(__file__))

        # Set up rate limiting
        limiter = Limiter(key_func=get_remote_address, default_limits=["2/second", "120/minute"])
        app.state.limiter = limiter
        app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
        app.add_middleware(SlowAPIMiddleware)
    except ImportError as e:
        print(e)

class Config():
    # Ensure the application is running in a virtual environment
    VirtualEnvironmentConfigConfig.ensure_virtualenv()
    root_path = os.getcwd()

    #Handle the parameters for the application
    exec_mudule = ArgConfig.args()


config = Config()           # Make accessible the config to access the paths and rules for the application
network = NetworkConfig()   # Used to configure the network for the FastAPI
env = EnvironmentConfig()   # Used to configure the environment for the application
