import time
import os
from datetime import datetime
from decimal import Decimal

import json
import boto3
from faker import Faker
from dotenv import load_dotenv


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(CustomEncoder, self).default(obj)

if __name__ == '__main__':
    
    num_events = 100

    fake = Faker(locale='pt_BR')
    load_dotenv('.env.dev.aws')
    
    aws_acess_key_id = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_key_id = os.getenv('AWS_SECRET_ACCESS_KEY')
    
    s3 = boto3.resource(
        's3', aws_access_key_id=aws_acess_key_id, 
        aws_secret_access_key=aws_secret_key_id
    )
    
    bucket_raw = os.environ.get('BUCKET_RAW')
    
    pages = [
        'home',
        'products',
        'product_details',
        'cart',
        'checkout',
        'profile'
    ]
    
    actions = [
        'view_page',
        'click_link',
        'add_to_cart',
        'remove_from_cart',
        'checkout',
        'purchase'
    ]
    
    if not os.path.exists("./json"):
        os.makedirs("./json")
        
    for i in range(num_events):
        user_data = {
            'id': fake.random_int(min=1, max=100),
            'name': fake.name(),
            'sex': fake.random_element(elements=('Male', 'Female')),
            'address': fake.address(),
            'ip': fake.ipv4(),
            'state': fake.state(),
            'latitude': fake.latitude(),
            'longitude': fake.longitude(),
    }
    
        event_data = {
            'timestamp': int(time.time()),
            'page': fake.random_element(elements=pages),
            'action': fake.random_element(elements=actions),
            'product_id': fake.random_int(min=1, max=100),
            'quantity': fake.random_int(min=1, max=5),
            'estoque_id': fake.random_int(min=1, max=100),
            'price': Decimal(str(round(fake.pyfloat(left_digits=2, right_digits=2, positive=True), 2))),
            'estoque_id_number': fake.random_int(min=1, max=100),
            'price': Decimal(str(round(fake.pyfloat(left_digits=2, right_digits=2, positive=True), 2)))
        }
    
        data = {
            'user': user_data,
            'event': event_data
        }
        
        now = datetime.now()
        frt_date = now.strftime("%d_%m_%Y_%H_%M_%S")
        
        with open(f'json/event_customers_mobile{i}_{frt_date}.json', 'w') as f:
            time.sleep(1)
            json.dump(data, f, cls=CustomEncoder)
        
        # time.sleep(3)
        s3.Object(bucket_raw, f'event_customers_mobile{i}_{frt_date}.json').put(Body=json.dumps(data, cls=CustomEncoder))