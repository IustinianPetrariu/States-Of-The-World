import requests
from requests.exceptions import HTTPError


def main():
    """
    Main function for testing API. Create a get response
    to API with a specific request
    :return: raw message received from API request
    """

    try:
        response = requests.get('http://127.0.0.1:5000/top-10-countries/density')
        response.raise_for_status()
        # access json content
        jsonResponse = response.json()
        print("JSON received from API:")
        print(jsonResponse)
    except HTTPError as server_err:
        print(f'HTTP error occurred: {server_err}')
    except Exception as error:
        print(f'Other error occurred: {error}')

    print("Print each key-value pair from JSON response")
    # for key, value in jsonResponse.items():
    #     print(key, ":", value)


if __name__ == "__main__":
    main()
