import logging
import datetime

from flask import request
from google.appengine.api import search, users
from google.appengine.ext import ndb

from core.utils import ok, create_json_response


def apply_search(blueprint, model, fields=None, paginate_limit=20):
    """    
    :param blueprint: blueprint object from Flask 
    :param model: model to inject the indexing of entities
    :param fields: array of entity properties that you want to be indexed, if None, all properties will be indexed.
    :return: none
    """

    @blueprint.route('/search', methods=['GET'])
    def api_search():
        """
         dynamic creation of api endpoint for search
        """
        query_string = request.args.get('query', None)
        cursor = request.args.get('cursor', None)
        q = search_index(model, paginate_limit=paginate_limit, query_string=query_string, cursor=cursor)
        return create_json_response(q)

    def inject_after_put(instance, entity):
        """
         dynamic creation of after_put method on assigned model
        """
        logging.info("creating index for entity %s" % str(entity))
        index(instance, only=fields)

    """
    inject to the model
    """
    model.after_put = inject_after_put


def search_index(Model, paginate_limit, query_string, cursor, index=None):
    """
    Searches using the provided index (or an automatically determine one).

    Expects the search query to be in the ``query`` request parameter.

    Also takes care of setting pagination information if the :class:`pagination component <ferris.components.pagination.Pagnation>` is present.
    """

    limit = paginate_limit
    response = dict()

    try:
        if cursor:
            cursor = search.Cursor(web_safe_string=cursor)
        else:
            cursor = search.Cursor()

        options = search.QueryOptions(
            limit=limit,
            ids_only=True,
            cursor=cursor)
        query = search.Query(query_string=query_string, options=options)

        if not index:
            if hasattr(Model, 'get_search_index'):
                index = Model.get_search_index()
            elif hasattr(Model, 'search_index_name'):
                index = Model.search_index_name
            else:
                index = 'auto_ix_%s' % Model._get_kind()
        index = search.Index(name=index)

        logging.debug("Searching %s with \"%s\" and cursor %s" % (index.name, query.query_string, cursor.web_safe_string))
        index_results = index.search(query)

        if issubclass(Model, ndb.Model):
            results = ndb.get_multi([ndb.Key(urlsafe=x.doc_id) for x in index_results])
            results = [x for x in results if x]
        else:
            results = Model.get([x.doc_id for x in index_results])
            Model.prefetch_references(results)

        if index_results.cursor:
            response['limit'] = limit
            response['cursor'] = cursor.web_safe_string
            response['next_cursor'] = str(index_results.cursor.web_safe_string())

    except (search.Error, search.query_parser.QueryException) as e:
        results = []
        logging.info("error occurred %s " % e)

    response['results'] = results
    return response


def index(instance, only=None, exclude=None, index=None, callback=None):
    """
    Adds an instance of a Model into full-text search.

    :param instance: an instance of ndb.Model
    :param list(string) only: If provided, will only index these fields
    :param list(string) exclude: If provided, will not index any of these fields
    :param index: The name of the search index to use, if not provided one will be automatically generated
    :param callback: A function that will recieve (instance, fields), fields being a map of property names to search.xField instances.

    This is usually done in :meth:`Model.after_put <ferris.core.ndb.Model.after_put>`, for example::

        def after_put(self):
            index(self)

    """

    if only:
        props = only
    else:
        props = instance._properties.keys()
        if exclude:
            props = [x for x in props if x not in exclude]

    if not index:
        index = 'auto_ix_%s' % instance.key.kind()
    index = search.Index(name=index)

    fields = {}
    for prop_name in props:
        if not hasattr(instance, prop_name):
            continue

        val = getattr(instance, prop_name)
        field = None
        is_text_field = False

        if isinstance(instance._properties[prop_name], ndb.BlobProperty) and not isinstance(instance._properties[prop_name], (ndb.StringProperty, ndb.TextProperty)):
            continue
        if isinstance(val, basestring):
            count = 0
            is_text_field = True
            iterate = True
            while iterate is True:
                name = prop_name + "_" + str(count)
                value = val[0:count+1]
                field = search.TextField(name=name, value=value)
                count += 1
                if value:
                    fields[name] = field

                if count > len(val):
                    iterate = False

        elif isinstance(val, datetime.datetime):
            field = search.DateField(name=prop_name, value=val.date())
        elif isinstance(val, datetime.date):
            field = search.DateField(name=prop_name, value=val)
        elif isinstance(val, users.User):
            field = search.TextField(name=prop_name, value=unicode(val))
        elif isinstance(val, bool):
            val = 'true' if val else 'false'
            field = search.AtomField(name=prop_name, value=val)
        elif isinstance(val, (float, int, long)):
            field = search.NumberField(name=prop_name, value=val)
        else:
            logging.debug('Property %s couldn\'t be added because it\'s a %s' % (prop_name, type(val)))

        if field and not is_text_field:
            fields[prop_name] = field

    if callback:
        callback(instance=instance, fields=fields)

    try:
        fields = fields.values()
        doc = search.Document(doc_id=str(instance.key.urlsafe()), fields=fields)
        index.put(doc)
    except:
        logging.error("Adding model %s instance %s to the full-text index failed" % (instance.key.kind(), instance.key.id()))
        logging.error([(x.name, x.value) for x in fields])


def unindex(instance_or_key, index=None):
    """
    Removes a document from the full-text search.

    This is usually done in :meth:`Model.after_delete <ferris.core.ndb.Model.after_delete>`, for example::

        @classmethod
        def after_delete(cls, key):
            unindex(key)

    """
    if isinstance(instance_or_key, ndb.Model):
        instance_or_key = instance_or_key.key

    if not index:
        index = 'auto_ix_%s' % instance_or_key.kind()
    index = search.Index(name=index)

    index.delete(str(instance_or_key.urlsafe()))
