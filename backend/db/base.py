from sqlalchemy.orm import declarative_base

# Base - это просто фабрика, от которой будут наследоваться все наши модели.
# Он не должен импортировать модели сам.
Base = declarative_base()