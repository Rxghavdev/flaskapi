from flask import Flask, jsonify
from pymongo import MongoClient
from mongoengine import connect, Document, StringField, BooleanField
from dotenv import load_dotenv
import os
load_dotenv()
app = Flask(__name__)

uri = f"mongodb+srv://{os.getenv('MONGO_USERNAME')}:{os.getenv('MONGO_PASSWORD')}@clusterappp.8u8wffp.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)

# Establish a default connection to the MongoDB database
connect(db='clusterapp', host=uri)

class Config(Document):
    service_url = StringField(required=True)
    Notification_custom_flag = BooleanField(default=False)
    Notification_custom_message = StringField()
    service_name = StringField(required=True)
    ad_id = StringField()
    android_link = StringField()
    ios_link = StringField()


@app.route('/')
def test_connection():
    try:
        client.server_info()  # Attempt to execute a MongoDB server command
        return jsonify({'message': 'Database connected'})
    except Exception as e:
        return jsonify({'message': 'Database connection failed', 'error': str(e)})

@app.route('/data', methods=['GET'])
def get_data():
    data = Config.objects().to_json()
    return jsonify(data)

@app.route('/post_config', methods=['POST'])
def post_config():
    sample_data = [
        {
            'service_url': 'https://example1.com',
            'Notification_custom_flag': True,
            'Notification_custom_message': 'Sample Message 1',
            'service_name': 'Service 1'
        },
        {
            'service_url': 'https://example2.com',
            'Notification_custom_flag': False,
            'Notification_custom_message': 'Sample Message 2',
            'service_name': 'Service 2'
        }
    ]

    for data in sample_data:
        config = Config(**data)
        config.save()

    return jsonify({'message': 'Sample data inserted'})

if __name__ == '__main__':
    app.run()
