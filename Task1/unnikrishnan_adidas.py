
import requests
import jsonlines


def main():

    url = 'https://www.adidas.co.th/api/stores' 

    params = {
        'sitePath':'en',
        'latitude':'13.736717',
        'longitude':'100.523186',
        'type':'4'

    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        'Accept-Language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Content-Type': 'application/json',
        'Accept': '*/*',  
    }

    response = requests.get(url, params=params, headers=headers)

    response.raise_for_status()

    print(response.status_code)

    print(response.json()['content'])
    
    output_file = 'unnikrishnan_adidas_stores.jsonl'

    with jsonlines.open(output_file, mode='w') as writer:
        for store in response.json()['content']:
            writer.write(store)
    
    print(f"Data saved to {output_file}")

if __name__ == '__main__':
    main()
