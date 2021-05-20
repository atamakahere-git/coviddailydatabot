import requests

API_LINK = "https://api.covid19india.org/csv/latest/case_time_series.csv"


def download_data():
    try:
        csv_data = requests.get(API_LINK)
        return csv_data.text.split('\n')[-2:]
    except Exception as e:
        print(e)
        print("Unable to download data")
        return None


def get_latest_data() -> str:
    d_data = download_data()
    data = d_data[1]
    prv_data = d_data[0]
    if data and prv_data:
        data_attr = data.split(',')
        prv_data_attr = prv_data.split(',')
        change = (int(prv_data_attr[2]) - int(data_attr[2])) * 100 / int(prv_data_attr[2])
        return f"Date : {data_attr[0]}\n" \
               f"Confirmed cases : {data_attr[2]}\n" \
               f"Recovered : {data_attr[4]}\n" \
               f"Deceased : {data_attr[6]}\n" \
               f"Change = {change:.2f}%"
    else:
        return "Unable to fetch data!"


def get_all_data() -> str:
    data = download_data()[1]
    if data:
        data_attr = data.split(',')
        return f"Date : {data_attr[0]}\n" \
               f"Total Confirmed cases : {data_attr[3]}\n" \
               f"Total Recovered : {data_attr[5]}\n" \
               f"Total Deceased : {data_attr[7]}"
    else:
        return "Unable to fetch data!"
