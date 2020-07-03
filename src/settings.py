class BaseConfig:
    redis_port = 6379
    redis_database = 0


class DevConfig(BaseConfig):
    redis_url = 'redis://0.0.0.0:6379/0'
    postgres_url = 'postgresql://db_user:123456@0.0.0.0:5432/image_microservice'
    redis_host = '0.0.0.0'


class ProdConfig(BaseConfig):
    redis_url = 'redis://redis_prod/0'
    postgres_url = 'postgresql://db_user:123456@db_prod/image_microservice_prod'
    redis_host = 'redis_prod'


class TestsConfig(BaseConfig):
    redis_url = 'redis://redis_test/0'
    postgres_url = 'postgresql://db_user:123456@db_test/image_microservice_test'
    redis_host = 'redis_test'


settings = ProdConfig()
