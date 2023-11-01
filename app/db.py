import os
from pymongo import MongoClient, errors
from .models import Notification, ReadNotify, Listing
from .send_email import Sender
import logging


def get_notification(notifications, limit, skip):
    result = []
    if skip >= len(notifications) or limit == 0:
        return None
    for notification in notifications[skip:]:
        result.append(notification)
        if len(result) == limit:
            return result
    return result


class Database:
    def __init__(self) -> None:
        self.client = MongoClient(os.getenv('DB_URI'))
        self.db = self.client['Users']
        self.sender = Sender()
        self.logger = logging.getLogger()

    def create(self, data: Notification):
        if data['key'] == 'registration':
            if data['data']['key']:
                return self.sender.send_email(data['data']['key'], data['user_id'])
            return self.sender.send_email(data['key'], data['user_id'])
        if data['key'] == 'new_login':
            if data['data']['key']:
                self.sender.send_email(data['data']['key'], data['user_id'])
            else:
                self.sender.send_email(data['key'], data['user_id'])
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
            return True

        except errors.DuplicateKeyError:
            self.logger.warning(f'{data["user_id"]} already exists')
            filt = {'_id': data['user_id']}
            new_value = {"$push": {'data': data['data']}}
            self.db[data['user_id']].update_one(filt, new_value)
            return True
        except Exception as e:
            self.logger.warning(f'Error occured while "create" request: {e}')

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
            self.logger.error(f'Error occured while "list" query:{e}')
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
            self.logger.error(f'Error occured while "read" query:{e}')
            return False
