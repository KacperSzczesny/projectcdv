import requests

def test_get_sensors():
    url = 
    response = requests.get(url)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)  

if __name__ == "__main__":
    test_get_sensors()
    print("Test passed!")
