import requests

def main():
    data = {
    'test1': '1',
    'test2': '0',
    }
    r = requests.post('http://localhost:8000/upload', data = "test.mp3")
    
if __name__ == "__main__":
    main()