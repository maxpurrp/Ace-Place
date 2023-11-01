from fastapi import APIRouter
from .models import Notification, ReadNotify, Listing
from .db import Database, get_notification
import logging


class Router:

    def __init__(self):
        self.router = APIRouter()
        self.db = Database()
        self.router.add_api_route("/", self.hello, methods=["GET"])
        self.router.add_api_route('/create', self._create, methods=['POST'], status_code =201)
        self.router.add_api_route('/read', self._read, methods=['POST'])
        self.router.add_api_route('/list', self._list, methods=['GET'])
        self.logger = logging.getLogger()

    async def hello(self):
        return {"Hello": 'world'}

    async def _create(self, notification: Notification):
        self.logger.info('Got request for creating notification')
        result = {"success": self.db.create(dict(notification))}
        self.logger.info(f'result is {result["success"]}')
        return {'success': result['success']}

    async def _read(self, read: ReadNotify):
        self.logger.info('Got request for read notification')
        result = {'success': self.db.read_notify(read)}
        self.logger.info(f'result is {result["success"]}')
        return {'success': result['success']}

    def _list(self, info: Listing):
        result = self.db.listing_notify(info)
        if result == False:
            return {'success': result}
        all_notification, new, res = result
        output_info = {
                'success': res,
                'data': {
                    'elements': len(all_notification),
                    'new': new,
                    'request': info,
                },
                'list': get_notification(all_notification,
                                      info.limit,
                                      info.skip)
            }
        return output_info
