class DBRouter(object):
  def db_for_read(self, model, **hints):
    if model._meta.app_label == 'weixin':
        return 'weixindb'
    return None

  def db_for_write(self, model, **hints):
    if model._meta.app_label == 'weixin':
        return 'weixindb'
    return None

  def allow_relation(self, obj1, obj2, **hints):
    if obj1._meta.app_label == 'weixin' or obj2._meta.app_label == 'weixin':
        return True
    return None

  def allow_syncdb(self, db, model):
    if db == 'weixindb':
        return model._meta.app_label == 'weixin'
    elif model._meta.app_label == 'weixin':
        return False
    return None
