def test_home(client):
    res = client.get("/")
    assert res.status_code == 200
    assert b"Bienvenido" in res.data


def test_test_route(client):
    res = client.get("/test")
    assert res.status_code == 200
    assert b"Ruta de prueba OK" in res.data
