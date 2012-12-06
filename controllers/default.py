# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################

def cdr():
    sqlgrid=SQLFORM.grid(db.cdr, fields=[db.cdr.calldate,
        db.cdr.clid,
        db.cdr.dst,
        db.cdr.dcontext,
        db.cdr.lastapp,
        db.cdr.billsec,
        db.cdr.disposition])
    #sqlgrid['_style']='border:1px solid red'
    #sqlgrid['_style']='font-size:11px'
    #sqlgrid['_style']='font-size:8px ;vertical-align:top; padding:1px 1px 1px 1px;'  
    return dict(sqlgrid=sqlgrid)

@auth.requires_login()
def extensions():
    sqlgrid=SQLFORM.grid(db.realtime_ext3)
    return dict(sqlgrid=sqlgrid)

def new_sip_user():
    form = crud.create(db.sip_conf_db, message='asdfasdfasd')
    return dict(form=form)

def new_sip_user_crud():
    form = crud.create(db.sip_conf_db)
    return dict(form=form)

def display_form():
    #form=FORM('ваше имя:', INPUT(_name='name'), INPUT(_type='submit'))
    record = db.sip_conf_db(request.args(0))
    form=SQLFORM(db.sip_conf_db, record, fields=['name','host','nat','type'],
        labels={'host':'host !'},
        col3={'name':A('what is this?', _href='http://www.google.com'), 'type':'can be peer or friend'},
        formstyle='table3cols'
        #formstyle=field_widget
        #_action='.',
        #_method= 'POST')
        )
    form.widgets.string.widget    
    if form.process().accepted:
        response.flash = 'user added'
    elif form.errors:
        response.flash = 'form has errors'
    return dict(form=form)

def display_manual_form():
    form = SQLFORM(db.sip_conf_db)
    if form.process(session=None, formname='test_form').accepted:
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'please fill the form'
    return dict()


def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simple replace the two lines below with:
    return auth.wiki()
    """
    #response.flash = T("Welcome to web2py!")
    #return dict(message=T('Hello World'))
    #
        #users=db().select(db.sip_conf_db.ALL, orderby=db.sip_conf_db.id)
    #return dict(users=users)
        #form = crud.select(db.sip_conf_db, fields=['name','host','nat','type'])
        #return dict(users=users, form=form)
    response.flash=T("hello to web2py")
    return dict (message='Asterisk configuration')           
    
@auth.requires_login()
def sql_form():
    sqlform=SQLFORM.grid(db.sip_conf_db, fields=[db.sip_conf_db.context,
        db.sip_conf_db.name,
        db.sip_conf_db.fullcontact,
        db.sip_conf_db.useragent])
    return dict(sqlform=sqlform)
    
def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request,db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


#@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())
