from __future__ import annotations

from app.classes import WithId

import os
import pickle
import logging
from typing import Final

class Repository:
    LOGGER = logging.getLogger(__name__)
    DB_ROOT_DIRECTORY: Final = os.path.dirname(os.path.abspath(__file__))
    TEMP_DIRECTORY_ABS_PATH: Final = os.path.join(DB_ROOT_DIRECTORY, "temp")

    def __init__(self) -> None:
        """ This class is not meant to be instantiated """
        pass

    @staticmethod
    def create_directory(directory: os.PathLike) -> None:
        if not os.path.exists(directory):
            try:
                os.makedirs(directory)
            except OSError as e:
                Repository.LOGGER.warning(f"Failed to create directory: {e.strerror}")

    @staticmethod
    def create_temp_directory() -> None:
        Repository.create_directory(Repository.TEMP_DIRECTORY_ABS_PATH)

    @staticmethod
    def get_object_file_path(_object: WithId, path: str = None) -> str:
        object_id = _object.get_id()
        directory_path = os.path.join(Repository.TEMP_DIRECTORY_ABS_PATH, path if path else _object.__class__.__name__)
        Repository.create_directory(directory_path)

        return os.path.join(directory_path, object_id)

    @staticmethod
    def _save_object(object: WithId, file: str) -> bool:
        if not os.path.exists(file):
            try:
                with open(file, "wb") as file:
                    pickle.dump(object, file)
                return True
            except Exception as e:
                Repository.LOGGER.warning(f"Failed to save object: {e}")
                return False

        Repository.LOGGER.warning("File already exists, use update method instead")
        return False

    @staticmethod
    def save(object: WithId, path: str = None) -> bool:
        object_path = Repository.get_object_file_path(object, path)
        return Repository._save_object(object, object_path)

    @staticmethod
    def load(path: str, id: str) -> WithId | None:
        _object: WithId | None = None
        directory = os.path.join(Repository.TEMP_DIRECTORY_ABS_PATH, path, id)
        try:
            with open(directory, "rb") as file:
                _object: WithId = pickle.load(file)
        except FileNotFoundError:
            Repository.LOGGER.warning(f"File not found {path}")
        except Exception as e:
            Repository.LOGGER.warning(f"Failed to load object: {e}")

        return _object

    @staticmethod
    def delete(object: WithId, path: str = None) -> bool:
        file = Repository.get_object_file_path(object, path)
        if os.path.exists(file):
            try:
                os.remove(file)
                return True
            except Exception as e:
                Repository.LOGGER.warning(f"Failed to delete file: {e}")
                return False

        return False

    @staticmethod
    def _update_object(object: WithId, object_path: str) -> bool:
        if os.path.exists(object_path):
            try:
                with open(object_path, "wb") as file:
                    pickle.dump(object, file)
                return True
            except Exception as e:
                Repository.LOGGER.warning(f"Failed to update object: {e}")
                return False

        return False

    @staticmethod
    def update(object: WithId, path: str = None) -> bool:
        object_path = Repository.get_object_file_path(object, path)
        return Repository._update_object(object, object_path)

    @staticmethod
    def load_all_object_in_directory(path: str) -> list[WithId]:
        directory = os.path.join(Repository.TEMP_DIRECTORY_ABS_PATH, path)
        objects: list[WithId] = []
        if os.path.exists(directory):
            for file in os.listdir(directory):
                try:
                    with open(os.path.join(directory, file), "rb") as file:
                        _object = pickle.load(file)
                        if isinstance(_object, WithId):
                            objects.append(_object)
                        else:
                            Repository.LOGGER.warning(f"Object is not an instance of WithId {_object}")
                except Exception as e:
                    Repository.LOGGER.warning(f"Failed to load object: {e}")

        return objects

    @staticmethod
    def set_debug_mode(debug: bool) -> None:
        Repository.LOGGER.disabled = not debug
