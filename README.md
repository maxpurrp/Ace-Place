# Приложение на FastAPI + MongoDB
 
Микросервис представляет из себя RestAPI сервер, который позволяет создавать запись уведомления пользователя в MongoDB, отправлять email пользователю, а также предоставлять листинг уведомлений из документа пользователя. 
### 1. /create
Данный эндпоинт позволяет сохранить уведомление(data) в документ пользователю. Так же в зависимости от ключа, который указан в уведомлении возможны несколько сценариев:
- registration (только отправит пользователю email)
- new_message (только создаст запись в документе пользователя)
- new_post (только создаст запись в документе пользователя)
- new_login (создаст запись в документе пользователя и отправит email)

Для корректной работы сервиса, который отправляет почту, рекомендуется использовать существующий email.


    	Method: Post
        		Path: http://localhost:8000/create
        		Headers: Content-type : json
        		Body: {
                    "user_id": "some_user_id",
                    "target_id": "0399ea67638f394d4b7243fc",
                    "key": "new_login",
                    "data": {
                        "id": "some_notification_id",
                        "timestamp": 1698138241,
                        "is_new": true,
                        "user_id": "some_user_id",
                        "key": "new_login",
                        "target_id": "0399ea67638f394d4b7243fc",
                        "data": {
                            "some_field": "some_value"
                        }}}
    	Response:
    		    Headers: Content-type: json
    	        HTTP Code 201
		        Body: {
                        "success": true
                    }
### 2. /list
Следующий эндпоинт позволяет просмотреть уведомления пользователя с указанием параметров, таких как skip(количество уведомлений, которые должны быть пропущены) и limit(количетсво уведомлений, которые следует вернуть)

    	Method: Post
        		Path: http://localhost:8000/list
        		Headers: Content-type : json
        		Body: {
                        "user_id": "some_user_id",
                        "skip": 1,
                        "limit": 2
                    }
    	Response:
    		    Headers: Content-type: json
    	        HTTP Code 200
		        Body: {
                        "success": true,
                        "data": {
                            "elements": 2,
                            "new": 2,
                            "request": {
                                "user_id": "some_user_id",
                                "skip": 1,
                                "limit": 2
                            }
                        },
                        "list": [
                            {
                                "id": "some_notification_id",
                                "timestamp": 1698138241,
                                "is_new": true,
                                "user_id": "some_user_id",
                                "key": "new_login",
                                "target_id": "0399ea67638f394d4b7243fc",
                                "data": {
                                    "some_field": "some_value"
                                }
                            },
                            {
                                "id": "some_notification_iD",
                                "timestamp": 1698138241,
                                "is_new": true,
                                "user_id": "some_user_id",
                                "key": "new_post",
                                "target_id": "0399ea67638f394d4b7243fc",
                                "data": {
                                    "some_field": "some_value"
                                }
                            }
                        ]
                    }
### 3. /read
Данный эндпоинт позволяет создать отметку о прочтении уведомления. В частности, у уведомления меняет поле ```is_new=true``` на ```is_new=false```.



    	Method: Post
        		Path: http://localhost:8000/read
        		Headers: Content-type : json
        		Body: {
                        "user_id":"some_user_id",
                        "notification_id": "some_notification_id"
                        }
    	Response:
    		    Headers: Content-type: json
    	        HTTP Code 200
		        Body: {
                        "success": true
                    }
### Использование
1. git clone https://github.com/maxpurrp/Ace-Place
2. cd Ace-Place
3. Настройте переменные окружения в файле ```docker-compose.yml``` в разделах ```environment```
    1. DB_URI - строка для подключения к mongoDB
    2. SMTP_HOST - хост smtp сервера
    3. SMTP_PORT - порт smtp сервера
    4. SMTP_LOGIN - логин пользователя
    5. SMTP_PASSWORD - пароль пользователя
    6. SMTP_EMAIL - email с которого будет отправлено сообщение
    7. MONGO_INITDB_ROOT_USERNAME -     Логин для базы данных
    8. MONGO_INITDB_ROOT_PASSWORD - пароль для базы данных
4. docker-compose up -d
5. Отправьте запросы используя вышеуказанные примеры для тестирования с помощью Postman или другое используемое вами приложение.
