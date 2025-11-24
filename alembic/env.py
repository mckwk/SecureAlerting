import glob
import importlib
import os
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config
from sqlalchemy import pool

from src.db.connection.connection import get_connection_string
from src.db.entities.base.base_entity import BaseEntity

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
model_files = glob.glob(
    os.path.join(
        os.path.dirname(__file__),
        '..',
        'src',
        'db',
        'entities',
        '**',
        '*.py'
    ),
    recursive=True
)

if model_files:
    for model_file in model_files:
        if model_file.endswith('__init__.py'):
            continue
        module_name = os.path.relpath(
            model_file,
            os.path.join(os.path.dirname(__file__), '..')
        ).replace(os.sep, '.')[:-3]
        module = importlib.import_module(module_name)

target_metadata = BaseEntity.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

def _check_sqlalchemy_url():
    url = config.get_main_option("sqlalchemy.url")
    if not url:
        config.set_main_option("sqlalchemy.url", get_connection_string())
    return url

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = _check_sqlalchemy_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    _check_sqlalchemy_url()

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
