import dotenv

dotenv.load_dotenv()
BOT_TOKEN = dotenv.get_key(dotenv_path=dotenv.find_dotenv(), key_to_get="BOT_TOKEN")
BOT_OWNER_ID = int(
    dotenv.get_key(
    dotenv_path=dotenv.find_dotenv(), key_to_get="BOT_OWNER_ID"
    )
)