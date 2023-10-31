

def get_notification(notifications, limit, skip):
    result = []
    if skip >= len(notifications) or limit == 0:
        return None
    for notification in notifications[skip:]:
        result.append(notification)
        if len(result) == limit:
            return result
    return result
