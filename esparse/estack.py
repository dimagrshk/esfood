from elasticsearch import Elasticsearch


def connect_elasticsearch():
    _es = None
    _es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    if _es.ping():
        print('Yay Connect')
    else:
        print('Awww it could not connect!')
    return _es


def store_record(elastic_object, index_name, record):
    try:
        return elastic_object.index(index=index_name, doc_type='salads', body=record)
    except Exception as ex:
        print('Error in indexing data')
        print(str(ex))


def create_index(es_object, index_name):
    settings = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0
        },
        "mappings": {
            "salads": {
                "dynamic": "strict",
                "properties": {
                    "title": {
                        "type": "text"
                    },
                    "description": {
                        "type": "text"
                    },
                    "calories": {
                        "type": "float"
                    },
                    "lipids": {
                        "type": "float"
                    },
                    "carbs": {
                        "type": "float"
                    },
                    "ingredients": {
                        "type": "nested",
                        "properties": {
                            "step": {"type": "text"}
                        }
                    },
                }
            }
        }
    }

    try:
        if not es_object.indices.exists(index_name):
            es_object.indices.create(index=index_name, ignore=400, body=settings)
            print('Created Index')
    except Exception as ex:
        print(str(ex))
