from datetime import date


class User(object):

    def __init__(self, uid, first_name, last_name):
        self.uid = uid
        self.first_name = first_name
        self.last_name = last_name
        self.sex = None
        self.relation = None
        self.is_exist_status = 0
        self.wall_len = None
        self.subscriptions = None
        self.photos = None
        self.number_of_friends = None

    def set_age(self, birth_date):
        if birth_date:
            self.age = int((date.today() - birth_date).days / 365.2425)

    def to_list(self):
        return [unicode(self.uid), self.first_name.encode('utf-8'), self.last_name.encode('utf-8'),
                           unicode(self.sex), unicode(self.relation), unicode(self.is_exist_status),
                           unicode(self.wall_len), unicode(self.subscriptions), unicode(self.photos),
                           unicode(self.number_of_friends)]
    def to_tsv(self):
        return u'\t'.join(self.to_list())
    def to_csv(self):
        return u','.join(self.to_list())
    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return u"User('{uid}', '{first}', '{last}')".format(uid=self.uid, first=self.first_name, last=self.last_name)
