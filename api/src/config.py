from pydantic import BaseModel, Field, ValidationError
from pydantic_yaml import parse_yaml_file_as


class DB(BaseModel):
    url: str = "sqlite:///test.db"
    log_sql: bool = True
    create_schema: bool = True
    create_testdata: bool = True


class Config(BaseModel):
    db: DB = Field(default_factory=lambda: DB())


def read_config() -> Config:
    return parse_yaml_file_as(Config, "api-config.yaml")


if __name__ == "__main__":
    try:
        config = read_config()
        print("config:", config)
        # print("config:", config.db.url)
    except ValidationError as error:
        print(error)
