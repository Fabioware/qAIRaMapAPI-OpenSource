import datetime
import dateutil
import dateutil.parser
import time
from project import app, db, socketio
from project.database.models import  Qhawax, QhawaxInstallationHistory
import project.main.util_helper as util_helper

session = db.session

def getQhawaxID(qhawax_name):
    """
    Helper function to get qHAWAX ID base on qHAWAX name

    :type qhawax_name: string
    :param qhawax_name: qHAWAX name

    """
    if(isinstance(qhawax_name, str)):
        qhawax_list = session.query(Qhawax.id).filter(Qhawax.name == qhawax_name).all()
        if(qhawax_list == []):
            raise TypeError("The qHAWAX name could not be found")
        qhawax_id = session.query(Qhawax.id).filter(Qhawax.name == qhawax_name).one()
        return qhawax_id
    else:
        raise TypeError("The qHAWAX name should be string")

def getQhawaxName(qhawax_id):
    """
    Helper function to get qHAWAX name base on qHAWAX ID

    :type qhawax_id: integer
    :param qhawax_id: qHAWAX ID

    """
    if(type(qhawax_id) not in [int]):
        raise TypeError("The qHAWAX id should be int")
    qhawax_list = session.query(Qhawax.name).filter(Qhawax.id == qhawax_id).all()
    if(qhawax_list == []):
        raise TypeError("The qHAWAX ID could not be found")
    return session.query(Qhawax.name).filter(Qhawax.id == qhawax_id).one() 


def getInstallationId(qhawax_id):
    if(type(qhawax_id) not in [int]):
        raise TypeError("The qHAWAX id should be int")
    installation_id= session.query(QhawaxInstallationHistory.id).filter_by(qhawax_id=qhawax_id). \
                                    filter(QhawaxInstallationHistory.end_date_zone == None). \
                                    order_by(QhawaxInstallationHistory.installation_date_zone.desc()).all()
    if(installation_id == []):
        return None

    return session.query(QhawaxInstallationHistory.id).filter_by(qhawax_id=qhawax_id). \
                                    filter(QhawaxInstallationHistory.end_date_zone == None). \
                                    order_by(QhawaxInstallationHistory.installation_date_zone.desc()).first()[0]

def getInstallationIdBaseName(qhawax_name):
    qhawax_id = getQhawaxID(qhawax_name)
    installation_id = getInstallationId(qhawax_id)
    return installation_id

