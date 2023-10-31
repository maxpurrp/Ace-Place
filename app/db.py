from pymongo import MongoClient, errors
from .models import Notification, ReadNotify, Listing
from .send_email import send_email
import logging


class Database:
    def __init__(self) -> None:
        self.client = MongoClient('mongodb://max:1234@mongodb:27017/')
        self.db = self.client['Users']
        self.logger = logging.getLogger()

    def create(self, data: Notification):
        if data['key'] == 'registration':
            if data['data']['key']:
                send_email(data['data']['key'], data['user_id'])
            else:
                send_email(data['key'], data['user_id'])
            return True
        if data['key'] == 'new_login':
            if data['data']['key']:
                send_email(data['data']['key'], data['user_id'])
            else:
                send_email(data['key'], data['user_id'])
        try:
            count = self.db[data['user_id']].find()
            if len(self.db.list_collection_names()) != 0:
                # CHECK LIMIT FOR NOTIFICATIONS
                if len(count[0]['data']) > 10:
                    return 'The limit for the number of notifications has been reached'
            self.db[data['user_id']].insert_one({'_id': data['user_id'],
                                                 'target_id': data['target_id'],
                                                 'key': data['key'],
                                                 'data': [data['data']]})

        except errors.DuplicateKeyError:
            self.logger.warning(f'{data["user_id"]} already exists')
            filt = {'_id': data['user_id']}
            new_value = {"$push": {'data': data['data']}}
            self.db[data['user_id']].update_one(filt, new_value)
        return True

    def listing_notify(self, info: Listing):
        all_notification = []
        new_notification = 0
        try:
            if len(self.db.list_collection_names()) != 0:
                collection = self.db[info.user_id].find({'_id': info.user_id})
                for notify in collection[0]['data']:
                    if notify['is_new']:
                        new_notification += 1
                    all_notification.append(notify)
                return (all_notification, new_notification, True)
            else:
                return False
        except Exception as e:
            self.logger.error(e)
            return False

    def read_notify(self, read: ReadNotify):
        try:
            if len(self.db.list_collection_names()) != 0:
                all_notification = self.db[read.user_id].find()
                for notify in all_notification[0]['data']:
                    if notify['id'] == read.notification_id:
                        filt = {'data.id': read.notification_id}
                        new_value = {"$set": {'data.$.is_new': False}}
                        self.db[read.user_id].find_one_and_update(filt, new_value)
                        return True
            return False
        except Exception as e:
            self.logger.error(e)
            return False
