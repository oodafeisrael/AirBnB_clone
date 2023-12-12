#!/usr/bin/python3
"""
Defines tests for models/engine/file_storage.py.
"""
import os
import pep8
import json
import models
import pytest
from datetime import datetime
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from models.user import User
from models.state import State
from models.place import Place
from models.city import City
from models.amenity import Amenity
from models.review import Review


@pytest.fixture
def setup_teardown():
    try:
        os.rename("file.json", "tmp")
    except IOError:
        pass

    yield

    try:
        os.remove("file.json")
    except IOError:
        pass
    try:
        os.rename("tmp", "file.json")
    except IOError:
        pass
    FileStorage._FileStorage__objects = {}


def test_pep8_conformance():
    style = pep8.StyleGuide(quiet=True)
    result = style.check_files(['models/engine/file_storage.py'])
    assert result.total_errors == 0, "Fix PEP8"


def test_file_storage_instantiation_no_args():
    assert type(FileStorage()) == FileStorage


def test_file_storage_instantiation_with_arg():
    with pytest.raises(TypeError):
        FileStorage(None)


def test_file_storage_file_path_is_private_str():
    assert type(FileStorage._FileStorage__file_path) == str


def test_file_storage_objects_is_private_dict():
    assert type(FileStorage._FileStorage__objects) == dict


def test_storage_initializes():
    assert type(models.storage) == FileStorage


def test_all():
    assert type(models.storage.all()) == dict


def test_all_with_arg():
    with pytest.raises(TypeError):
        models.storage.all(None)


def test_new():
    bm = BaseModel()
    us = User()
    st = State()
    pl = Place()
    cy = City()
    am = Amenity()
    rv = Review()
    models.storage.new(bm)
    models.storage.new(us)
    models.storage.new(st)
    models.storage.new(pl)
    models.storage.new(cy)
    models.storage.new(am)
    models.storage.new(rv)
    assert f"BaseModel.{bm.id}" in models.storage.all().keys()
    assert bm in models.storage.all().values()
    assert f"User.{us.id}" in models.storage.all().keys()
    assert us in models.storage.all().values()
    assert f"State.{st.id}" in models.storage.all().keys()
    assert st in models.storage.all().values()
    assert f"Place.{pl.id}" in models.storage.all().keys()
    assert pl in models.storage.all().values()
    assert f"City.{cy.id}" in models.storage.all().keys()
    assert cy in models.storage.all().values()
    assert f"Amenity.{am.id}" in models.storage.all().keys()
    assert am in models.storage.all().values()
    assert f"Review.{rv.id}" in models.storage.all().keys()
    assert rv in models.storage.all().values()


def test_new_with_args():
    with pytest.raises(TypeError):
        models.storage.new(BaseModel(), 1)


def test_save():
    bm = BaseModel()
    us = User()
    st = State()
    pl = Place()
    cy = City()
    am = Amenity()
    rv = Review()
    models.storage.new(bm)
    models.storage.new(us)
    models.storage.new(st)
    models.storage.new(pl)
    models.storage.new(cy)
    models.storage.new(am)
    models.storage.new(rv)
    models.storage.save()
    save_text = ""
    with open("file.json", "r") as f:
        save_text = f.read()
        assert f"BaseModel.{bm.id}" in save_text
        assert f"User.{us.id}" in save_text
        assert f"State.{st.id}" in save_text
        assert f"Place.{pl.id}" in save_text
        assert f"City.{cy.id}" in save_text
        assert f"Amenity.{am.id}" in save_text
        assert f"Review.{rv.id}" in save_text


def test_save_with_arg():
    with pytest.raises(TypeError):
        models.storage.save(None)


def test_reload(setup_teardown):
    a_storage = FileStorage()
    try:
        os.remove("file.json")
    except FileNotFoundError:
        pass
    with open("file.json", "w") as f:
        f.write("{}")
    with open("file.json", "r") as r:
        for line in r:
            assert line == "{}"
    assert a_storage.reload() is None


def test_reload_with_arg():
    with pytest.raises(TypeError):
        models.storage.reload(None)


if __name__ == "__main__":
    unittest.main()
