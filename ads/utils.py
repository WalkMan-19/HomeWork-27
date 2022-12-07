import json
import csv

ADS_DATA = "../datasets/ads.csv"
CATEGORIES_DATA = "../datasets/categories.csv"


def read_file(data, json_file, model):
    result = []
    try:
        with open(data, 'r', encoding='utf-8') as f:
            for line in csv.DictReader(f):
                add_to_dict = {
                    'model': model,
                    'pk': int(line['Id'] if 'Id' in line else line['id']),
                }
                if 'id' in line:
                    del line['id']
                else:
                    del line['Id']

                if "is_published" in line:
                    if line["is_published"] == 'TRUE':
                        line["is_published"] = True
                    else:
                        line["is_published"] = False

                if "price" in line:
                    line["price"] = int(line["price"])

                add_to_dict['fields'] = line
                result.append(add_to_dict)

        with open(json_file, 'w', encoding='utf-8') as j_f:
            j_f.write(json.dumps(result, ensure_ascii=True))

    except ValueError as e:
        print(e)
    except FileNotFoundError as e:
        print(e)


if __name__ == '__main__':
    read_file(data=ADS_DATA, json_file="../datasets/ads.json", model="ads.ad")
    read_file(data=CATEGORIES_DATA, json_file="../datasets/categories.json", model="ads.category")

