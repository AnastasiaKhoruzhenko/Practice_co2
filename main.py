import sqlite3
from flask import Flask, request, jsonify, abort

app = Flask(__name__)


@app.route('/api/co2')
def co2_list():
    aircraft_codes = get_splitted_array('aircraft')
    km = get_splitted_array('distance')

    if len(aircraft_codes) != len(km):
        abort(400)

    result = get_info_from_database(aircraft_codes, km)
    return jsonify(result)


def get_splitted_array(value):
    return str(request.args.get(value)).split(',')


def get_info_from_database(aircraft_codes, km):
    db = sqlite3.connect('newDatabase.db')

    result = []

    a = 0
    for item in aircraft_codes:
        response = {}
        with db:
            cursor = db.cursor()
            cursor.execute('SELECT * FROM database WHERE Code=?', (item,))
            row = cursor.fetchone()
            # if there is no such aircraft code in database
            if row is None:
                abort(400)

            table = get_km_row(km[a])

            # if there is no such km value or None kg value in database
            if table is -1 or row[table] is None:
                abort(400)

            response['Aircraft_number'] = item
            response['km'] = km[a]
            co2 = row[table]
            response['co2'] = co2
            result.append(response)
            a = a + 1
    return result


def get_km_row(temp):
    km_dict = {
        '125': 1,
        '250': 2,
        '500': 3,
        '750': 4,
        '1000': 5,
        '1500': 6,
        '2000': 7,
        '2500': 8,
        '3000': 9,
        '3500': 10,
        '4000': 11,
        '4500': 12,
        '5000': 13,
        '5500': 14,
        '6000': 15,
        '6500': 16,
        '7000': 17,
        '7500': 18,
        '8000': 19,
        '8500': 20,
    }
    return km_dict.get(temp, -1)


if __name__ == '__main__':
    app.run()
