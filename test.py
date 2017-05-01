import os

data = [
    {
        u'wake_up_time': u'0700',
        u'on': True,
        u'wake_up_days': [u'0',
                          u'1',
                          u'2'],
        u'name': u'School',
        u'wake_up_threshold': u'10',
        u'userId': u'jQtqihWFAi4bSkoWr',
        u'_id': u'hhFwucWcZumWbZjTi'
    },
    {
        u'wake_up_time': u'1800',
        u'on': True,
        u'wake_up_days': [u'4'],
        u'name': u'Party',
        u'wake_up_threshold': u'10',
        u'userId': u'jQtqihWFAi4bSkoWr',
        u'_id': u'QMgmNJjBMe29Wouoq'
    },
    {
        u'wake_up_time': u'1200',
        u'on': True,
        u'wake_up_days': [u'0',
                          u'1',
                          u'2',
                          u'3'],
        u'name': u'test',
        u'wake_up_threshold': u'15',
        u'userId': u'bp3XGWYMHds63pi49',
        u'_id': u'x3Fas3c5jrEnoFsp9'
    }
]

users = {}

for alarm in data:
    if users.get(alarm["userId"]):
        users.get(alarm["userId"]).append(alarm)
    else:
        users[alarm["userId"]] = [alarm]


# os.makedirs("users")                             # create directory [current_path]/feed/address
# dir_path = os.path.join("users", self.address)

for user in users:
    # print(user)
    print( user +":" + str(users[user]))
    file_name = user +".json"
    file_ = open(os.path.join("users", file_name), 'wb')
