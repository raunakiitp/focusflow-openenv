import requests

def test_api():
    print("Testing /reset endpoint...")
    # HF spaces URL: https://raunakiitp-focusflow-env.hf.space
    url = "https://raunakiitp-focusflow-env.hf.space/reset"
    
    try:
        response = requests.post(url, json={})
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print("SUCCESS! The HF Space is alive and accepts POST /reset correctly.")
        else:
            print(f"FAIL: Returned {response.status_code}")
            print(response.text)
    except Exception as e:
         print("Error reaching space:", e)

if __name__ == "__main__":
    test_api()
