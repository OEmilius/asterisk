# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

db = DAL('mysql://testuser:topsecret@localhost:3306/webtopy')
#https://wiki.asterisk.org/wiki/display/AST/MySQL+CDR+Backend
db.define_table('cdr',
    Field('calldate', 'datetime', notnull=True),#, default='0000-00-00 00:00:00'),
    Field('clid', length=80, notnull=True, default=''),
    Field('src', length=80, notnull=True, default=''),
    Field('dst', length=80, notnull=True, default=''),
    Field('dcontext', length=80, notnull=True, default=''),
    Field('channel', length=80, notnull=True, default=''),
    Field('dstchannel', length=80, notnull=True, default=''),
    Field('lastapp', length=80, notnull=True, default=''),
    Field('lastdata', length=80, notnull=True, default=''),
    Field('duration', 'integer', notnull=True, default='0'),
    Field('billsec', 'integer', notnull=True, default='0'),
    Field('disposition', length=45, notnull=True, default='0'),
    Field('amaflags', 'integer', notnull=True, default='0'),
    Field('accountcode', length=20, notnull=True, default=''),
    Field('uniqueid', length=32, notnull=True, default=''),
    Field('userfield', length=255, notnull=True, default=''),
    Field('sequence', 'integer', notnull=True, default='0'),
    Field('linkedid', length=32, notnull=True, default=''),
    Field('peeraccount', length=20, notnull=True, default=''))

#get from https://wiki.asterisk.org/wiki/display/AST/SIP+Realtime%2C+MySQL+table+structure
db.define_table('sip_conf_db',
    Field('name', length=80, notnull=True, unique=True),
    Field('host', length=31, notnull=True, default='dynamic', requires=IS_NOT_EMPTY(error_message='cannot be empty')),
    Field('nat', length=5, notnull=True, default='no',requires=IS_IN_SET(['yes','no'])),
    Field('type', length=7, notnull=True, default='friend'),
    Field('accountcode', length=20, default='ACCOUNT'),
    Field('amaflags', length=13, default='billing'), #can be default='default'
    Field('callgroup', length=10),
    Field('callerid', length=80),
    #Field('call-limit', 'integer', notnull=True, default='3'),#deprecated
    Field('cancallforward', length=3, default='yes'),
    Field('canreinvite', length=3, default='no'),
    Field('context', length=80, default='from-internal'),
    Field('defaultip', length=15),
    Field('dtmfmode', length=8, default='rfc2833', requires=IS_IN_SET(['rfc2833','info','shortinfo','inband','auto'])),
    Field('fromuser', length=80),
    Field('fromdomain', length=80),
    Field('insecure', length=4),
    Field('language', length=2, default='ru'),
    Field('mailbox', length=50),
    Field('md5secret', length=80),
    Field('deny', length=95, default='0.0.0.0/0.0.0.0'),
    Field('permit', length=95, default='0.0.0.0/0.0.0.0'),
    Field('mask', length=95),
    Field('musiconhold', length=100, default='default'),
    Field('pickupgroup', length=10),
    Field('qualify', length=30, default='0'),
    Field('regexten', length=80),
    Field('restrictcid', 'integer', default='0'),
    Field('rtptimeout', 'integer', default='0'),
    Field('rtpholdtimeout', 'integer', default='0'),
    Field('secret', length=80, default='SECRET'),
    Field('setvar', length=100),
    Field('disallow', length=100, default='all'),
    Field('allow', length=100, default='alaw;ulaw;gsm'),
    Field('fullcontact', length=80, default=''),
    Field('ipaddr', length=45, default=''),
    Field('port', 'integer', notnull=True, default='0'),
    Field('regserver', length=100),
    Field('regseconds', 'integer', notnull=True, default='0'),
    #Field('username', length=80, notnull=True),
    Field('defaultuser', length=80, notnull=True),
    Field('subscribemwi', length=10, default='yes'),
    Field('allowsubscribe', length=3, default='yes', requires=IS_IN_SET(['yes','no'])),
    Field('subscribecontext', length=80),
    Field('notifyhold', length=10, default='yes'),
    Field('notifycid', length=10, default='yes'),
    Field('notifyringing', length=10, default='yes'),
    Field('useragent', length=20),
    Field('lastms', length=11))
    
db.define_table('realtime_ext3',
    #Field('id', 'integer'),
    Field('context', length=20, notnull=True, default=''),
    Field('exten', length=20, notnull=True, default=''),
    Field('priority', 'integer', notnull=True, default='0'),
    Field('app', length=20, notnull=True, default=''),
    Field('appdata', length=128, notnull=True, default=''))
    #primarykey=['context', 'exten', 'priority'])

#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Crud, Service, PluginManager, prettydate
auth = Auth(db)
crud, service, plugins = Crud(db), Service(), PluginManager()

## create all tables needed by auth if not custom tables
auth.define_tables(username=False, signature=False)

## configure email
mail=auth.settings.mailer
mail.settings.server = 'logging' or 'smtp.gmail.com:587'
mail.settings.sender = 'you@gmail.com'
mail.settings.login = 'username:password'

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

## if you need to use OpenID, Facebook, MySpace, Twitter, Linkedin, etc.
## register with janrain.com, write your domain:api_key in private/janrain.key
from gluon.contrib.login_methods.rpx_account import use_janrain
use_janrain(auth,filename='private/janrain.key')

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

## after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)
