from flask import Flask, request
import mongoengine
import json
import threading

app = Flask(__name__)
mongoengine.connect('average_app_db', host='localhost', port=27017)


class Customer(mongoengine.Document):
    name = mongoengine.StringField(required=True, max_length=100)
    time_values_reference = mongoengine.DictField()

    def __repr__(self):
        return str({'name': self.name, 'tv_range': self.time_values_reference})


class Request(mongoengine.Document):
    status = mongoengine.StringField(required=True)
    value = mongoengine.DictField()

    def __repr__(self):
        return str({'status': self.status, 'value': self.value})


@app.route('/api/health', methods=['GET'])
def health():
    return {}, 200

@app.route('/api/add_customers', methods=['POST'])
def get_customers():
    for data in request.json:
        print(f'data :: {data}')
        found_customer = Customer.objects.filter(name=data['name']).first()
        if not found_customer:
            found_customer = Customer(name=data['name'], time_values_reference={str(data['t']): str(data['v'])})
        else:
            found_customer.time_values_reference[str(data['t'])] = str(data['v'])
        found_customer.save()

    return {'Accepted': 201}, 201

@app.route('/api/get_average/<customer_name>/<from_range>/<to_range>', methods=['GET'])
def get_customer_by_name(customer_name, from_range, to_range):
    if not Customer.objects.filter(name=customer_name).first():
        return str({'error': 'Customer not found'}), 404
    if to_range < from_range:
        return str({'error': 'Time range is incorrect'}), 406
    new_request = Request(status='In progress', value={'s':0.0, 'a':0.0})
    new_request.save()
    x = threading.Thread(target=get_customer_average, args=(new_request.id, customer_name,from_range,to_range,))
    x.start()
    return str({'requestID': str(new_request.id)})

@app.route('/api/request/<requestID>', methods=['GET'])
def get_request(requestID):
    return Request.objects.filter(_id=requestID).first()

def get_customer_average(requestID, customer_name, from_range, to_range):
    found_customer = Customer.objects.filter(name=customer_name).first()
    customer_sum = 0.0
    number_of_elements = 0
    for k, v in found_customer['time_values_reference'].items():
        if int(from_range) <= int(k) <= int(to_range):
            customer_sum += float(v)
            number_of_elements += 1

    customer_average = customer_sum / number_of_elements
    found_request = Request.objects(id=requestID).first()
    print(f'found request :: {type(found_request)}')
    found_request.value['s'] = customer_sum
    found_request.value['a'] = customer_average
    found_request.status = 'Done'
    found_request.save()



if __name__ == '__main__':
    app.run(debug=True)