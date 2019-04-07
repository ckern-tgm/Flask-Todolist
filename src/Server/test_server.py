import pytest
import Server
import json


@pytest.fixture
def client():
    app = Server.app.test_client()
    return app

#####################################################################
# Test get function
def test_server_up(client):
    client.post("/todos", data={
        "task": "Write Tests"
    })
    res = client.get("/todos")
    assert len(res.json) > 0

def test_get_todos_exist(client):
    response = client.get("/todos")
    assert response.status_code == 200

def test_get_sepcific_todo(client):
    res = client.get("/todos/todo1")
    assert res.status_code == 201


#####################################################################
# Test post function
def test_post_empty(client):
    response = client.post("/todos", data={
        "task": None
    })
    assert response.json == "enter description"

def test_post_okay(client):
    response = client.post("/todos", data={
        "task": "Write Testcases"
    })
    assert response.json == "Todo added"

def test_post_statuscode(client):
    response = client.post("/todos", data={
        "task": "Write Testcases"
    })
    assert response.status_code == 201

def test_post_works(client):
    res1 = client.get("/todos")
    client.post("/todos", data={
        "task": "Write Tests"
    })
    res2 = client.get("/todos")
    assert len(res1.json) < len(res2.json)

#####################################################################
# Test delete function
def test_delete_item_doesnt_exist(client):
    client.post("/todos", data={
        "task": "Write Tests"
    })
    res = client.delete("/todos/2")
    assert res.status_code == 404

def test_delete_item_ok(client):
    client.post("/todos", data={
        "task": "Write Tests"
    })
    res = client.delete("/todos/todo2")
    assert res.status_code == 204

def test_delete_works(client):
    res = client.get("/todos")
    client.delete("/todos/todo3")
    client.delete("/todos/todo4")
    client.delete("/todos/todo5")
    client.delete("/todos/todo6")
    client.delete("/todos/todo7")
    res2 = client.get("/todos")
    assert len(res.json) > len(res2.json)


#####################################################################
# Test put function

def test_put_item_doesnt_exist(client):
    res = client.delete("/todos/1")
    assert res.status_code == 404

def test_put_item_ok(client):
    res = client.put("/todos/todo1", data={
        "task" : "updated Task"
    })
    assert res.status_code == 201

def test_put_works(client):
    res = client.get("/todos")
    client.put("/todos/todo1", data={
        "task" : "updated Task"
    })
    res2 = client.get("/todo")
    assert res.json != res2.json