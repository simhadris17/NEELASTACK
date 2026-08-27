import os

from packages.neelastack.database.base import Base
from packages.neelastack.database.session import engine
import packages.neelastack.database.models  # noqa: F401


def main() -> None:
    Base.metadata.create_all(engine)
    os.execvp(
        "uvicorn",
        ["uvicorn", "apps.api.main:app", "--host", "0.0.0.0", "--port", "8000"],
    )


if __name__ == "__main__":
    main()
