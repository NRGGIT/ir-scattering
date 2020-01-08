import csv
def csv_to_dict(path):
    # удобнее работать пока с данными,
    # получаемыми итератором из csv,
    # потом надо будет доставать данные
    # целиком и читать это как вектора

    with open(path, 'r') as csv_file:
        reader = csv.reader(csv_file)
        len(next(reader))
        abs_func = {}
        for row in reader:
            pair = row[0].replace(',', '.').split(';')
            abs_func[float(pair[0])] = float(pair[1])
        return abs_func


def csv_reader(path):
    csv_file = open(path, 'r')
    reader = csv.reader(csv_file)
    pair = next(reader)[0].split(';')
    return float(pair[0]), float(pair[1])

