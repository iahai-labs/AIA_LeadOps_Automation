from app.db import init_db


def test_init_db_module_exposes_initializer() -> None:
    assert callable(init_db.init_db)
