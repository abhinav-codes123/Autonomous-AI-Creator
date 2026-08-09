from app.core.config import Settings

def test_database_url_validation_postgres():
    s1 = Settings(DATABASE_URL="postgres://user:password@ep-host.render.com:5432/dbname")
    assert s1.DATABASE_URL == "postgresql+asyncpg://user:password@ep-host.render.com:5432/dbname"

    s2 = Settings(DATABASE_URL="postgresql://user:password@ep-host.render.com:5432/dbname")
    assert s2.DATABASE_URL == "postgresql+asyncpg://user:password@ep-host.render.com:5432/dbname"

    s3 = Settings(DATABASE_URL="postgresql+asyncpg://user:password@ep-host.render.com:5432/dbname")
    assert s3.DATABASE_URL == "postgresql+asyncpg://user:password@ep-host.render.com:5432/dbname"

def test_database_url_validation_sqlite():
    s1 = Settings(DATABASE_URL="sqlite:///./test.db")
    assert s1.DATABASE_URL == "sqlite+aiosqlite:///./test.db"

    s2 = Settings(DATABASE_URL="sqlite+aiosqlite:///./test.db")
    assert s2.DATABASE_URL == "sqlite+aiosqlite:///./test.db"
