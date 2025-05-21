# Imports do sistema
from logging.config import fileConfig
from os import path

# Imports de terceiros
from alembic import context
from dotenv import load_dotenv
from sqlalchemy import engine_from_config, pool

# Imports locais
from core.config import settings
from core.database import Base
from src.models.client_model import ClientModel
from src.models.order_item_model import OrderItemModel
from src.models.order_model import OrderModel
from src.models.product_model import ProductModel
from src.models.user_model import UserModel

load_dotenv(path.join(path.dirname(__file__), '../env/.env'))

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """
    Run migrations in 'offline' mode.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """
    Run migrations in 'online' mode.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
