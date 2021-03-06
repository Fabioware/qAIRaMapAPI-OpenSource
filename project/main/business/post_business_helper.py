import datetime
import dateutil
import dateutil.parser
from project import app, db
import project.main.util_helper as util_helper
import project.main.same_function_helper as same_helper
import project.main.business.get_business_helper as get_business_helper
from project.database.models import GasSensor, Qhawax, EcaNoise, QhawaxInstallationHistory, \
                                    Company, AirQualityMeasurement, Bitacora

var_gases=['CO','H2S','NO','NO2','O3','SO2']
session = db.session

def updateJsonGasSensor(qhawax_name, json_gas_sensor):
    """
    Helper Gas Sensor function to save json from qHAWAX ID

    """
    if(isinstance(json_gas_sensor, dict) is not True):
        raise TypeError("Gas Sensor Variables "+str(json_gas_sensor)+" should be Json Format")
    qhawax_id = same_helper.getQhawaxID(qhawax_name)
    if(qhawax_id is not None):
        for sensor_type in json_gas_sensor:
            session.query(GasSensor).filter_by(qhawax_id=qhawax_id, type=sensor_type).\
                                     update(values=json_gas_sensor[sensor_type])
        session.commit()

def updateMainIncaQhawaxTable(new_main_inca, qhawax_name):
    """
    Helper qHAWAX function to save main inca value in qHAWAX table

    """
    if(type(new_main_inca) not in [int]):
        raise TypeError("Inca value "+str(new_main_inca)+" should be int")

    if(same_helper.qhawaxExistBasedOnName(qhawax_name)):
        session.query(Qhawax).filter_by(name=qhawax_name).update(values={'main_inca': new_main_inca})
        session.commit()

def updateMainIncaQhawaxInstallationTable(new_main_inca, qhawax_name):
    """
    Helper qHAWAX function to save main inca value in qHAWAX Installation table

    """
    if(type(new_main_inca) not in [int]):
        raise TypeError("Inca value "+str(new_main_inca)+" should be int")

    if(same_helper.qhawaxExistBasedOnName(qhawax_name)):
        installation_id=same_helper.getInstallationIdBaseName(qhawax_name)
        session.query(QhawaxInstallationHistory).filter_by(id=installation_id).\
                                                 update(values={'main_inca': new_main_inca})
        session.commit()

def saveStatusOffQhawaxTable(qhawax_name):
    """
    Set qHAWAX OFF in qHAWAX table

    """
    if(same_helper.qhawaxExistBasedOnName(qhawax_name)):
        session.query(Qhawax).filter_by(name=qhawax_name).\
                              update(values={'state': "OFF",'main_inca':-1})
        session.commit()

def saveStatusOffQhawaxInstallationTable(qhawax_name,qhawax_lost_timestamp):
    """
    Set qHAWAX OFF in qHAWAX Installation table

    """
    installation_id=same_helper.getInstallationIdBaseName(qhawax_name)
    if(installation_id is not None):
        session.query(QhawaxInstallationHistory).\
                filter_by(id=installation_id).\
                update(values={'main_inca': -1,'last_registration_time_zone':qhawax_lost_timestamp})
        session.commit()

def saveStatusOnTable(qhawax_name):
    """
    Set qHAWAX ON in qHAWAX table

    """
    if(same_helper.qhawaxExistBasedOnName(qhawax_name)):
        session.query(Qhawax).filter_by(name=qhawax_name).update(values={'state': "ON",'main_inca':0})
        session.commit()

def saveTurnOnLastTime(qhawax_name):
    """
    Set qHAWAX ON in qHAWAX Installation table

    """
    installation_id = same_helper.getInstallationIdBaseName(qhawax_name)
    if(installation_id is not None):
        now = datetime.datetime.now(dateutil.tz.tzutc())
        session.query(QhawaxInstallationHistory).\
                filter_by(id=installation_id).\
                update(values={'main_inca': 0, \
                               'last_time_physically_turn_on_zone': now.replace(tzinfo=None)})
        session.commit()

def turnOnAfterCalibration(qhawax_name):
    """
    Set qHAWAX ON in qHAWAX Installation table

    """
    installation_id = same_helper.getInstallationIdBaseName(qhawax_name)
    if(installation_id is not None):
        now = datetime.datetime.now(dateutil.tz.tzutc())
        session.query(QhawaxInstallationHistory).\
                filter_by(id=installation_id).\
                update(values={'last_time_physically_turn_on_zone': now.replace(tzinfo=None)})
        session.commit()


def setOccupiedQhawax(qhawax_id):
    """
    Update qHAWAX Availability to Occupied

    """
    if(same_helper.qhawaxExistBasedOnID(qhawax_id)):
        session.query(Qhawax).filter_by(id=qhawax_id).update(values={'availability': 'Occupied'})
        session.commit()

def setModeCustomer(qhawax_id):
    """
    Update qHAWAX mode to Customer

    """
    if(same_helper.qhawaxExistBasedOnID(qhawax_id)):
        session.query(Qhawax).filter_by(id=qhawax_id).update(values={'mode': "Cliente"})
        session.commit()

def saveEndWorkFieldDate(qhawax_id,end_date,date_format):
    """
    Save End Work in Field

    """
    util_helper.check_valid_date(end_date,date_format)
    
    if(same_helper.qhawaxExistBasedOnID(qhawax_id)):
        installation_id = same_helper.getInstallationId(qhawax_id)
        session.query(QhawaxInstallationHistory).filter_by(id=installation_id).\
                                                 update(values={'end_date_zone': end_date})
        session.commit()

def setAvailableQhawax(qhawax_id):
    """
    Update qhawax installation state in qHAWAX table

    """
    if(same_helper.qhawaxExistBasedOnID(qhawax_id)):
        session.query(Qhawax).filter_by(id=qhawax_id).update(values={'availability': 'Available'})
        session.commit()


def changeMode(qhawax_name, mode):
    """
    Change To Other Mode

    """
    if(isinstance(mode, str) is not True):
        raise TypeError("Mode value "+str(mode)+" should be string")

    if(same_helper.qhawaxExistBasedOnName(qhawax_name)):
        session.query(Qhawax).filter_by(name=qhawax_name).update(values={'mode': mode})
        session.commit()

def updateQhawaxInstallation(data):
    """
    Update qHAWAX in Field 

    """
    if(isinstance(data, dict)):
        if(util_helper.areFieldsValid(data)==True):
            session.query(QhawaxInstallationHistory). \
                    filter_by(qhawax_id=data['qhawax_id'], \
                              company_id=data['company_id'], \
                              end_date_zone=None).update(values=data)
            session.commit()
        else:
            raise Exception("qHAWAX Installation fields must have data")
    else:
        raise TypeError("qHAWAX Installation data "+str(data)+" should be in Json Format")

def createQhawax(qhawax_name,qhawax_type):
    """
    Create a qHAWAX module 
    """
    qhawax_id = 1
    last_qhawax_id = get_business_helper.queryGetLastQhawax()
    
    if(last_qhawax_id!=None):
        qhawax_id = int(last_qhawax_id[0])+1
    
    if(isinstance(qhawax_name, str) and isinstance(qhawax_type, str)):
        qhawax_data = {'id':qhawax_id,'name': qhawax_name, 'qhawax_type': qhawax_type,
                       'state': 'OFF', 'availability': "Available", 'main_inca':-1.0, 
                       'main_aqi':-1.0,'mode':"Stand By"}
        qhawax_data_var = Qhawax(**qhawax_data)
        session.add(qhawax_data_var)
        session.commit()
    else:
        raise TypeError("qHAWAX name and type should be string")


def insertDefaultOffsets(qhawax_name):
    """
    To insert a Default Offset 

    """
    last_gas_sensor_id = 0
    last_gas_sensor = get_business_helper.queryGetLastGasSensor()

    if(last_gas_sensor!=None):
        last_gas_sensor_id= last_gas_sensor[0]

    if(same_helper.qhawaxExistBasedOnName(qhawax_name)):
        qhawax_id = int(same_helper.getQhawaxID(qhawax_name))
        initial_serial_number = qhawax_id*100
        start = 1
        for index in range(len(var_gases)):
            sensor_data = {'id':last_gas_sensor_id+start, 'qhawax_id':qhawax_id, 
                           'serial_number': initial_serial_number + start, 'type': var_gases[index],
                           'WE': 0.0, 'AE': 0.0,'sensitivity': 0.0, 'sensitivity_2': 0.0,
                           'C0':0.0,'C1':0.0,'C2':0.0,'NC0':0.0,'NC1':0.0}
            sensor_data_var = GasSensor(**sensor_data)
            session.add(sensor_data_var)
            session.commit()
            start+=1

def createCompany(json_company):
    """
    To insert new company

    """
    if(isinstance(json_company, dict) is not True):
        raise TypeError("The Json company "+str(json_company)+" should be in Json Format")

    company_name = json_company.pop('company_name', None)
    json_company['name'] = company_name
    company_var = Company(**json_company)
    session.add(company_var)
    session.commit()

def storeNewQhawaxInstallation(data):
    """
    Insert new qHAWAX in Field 

    """
    if(isinstance(data, dict)):
        if(util_helper.areFieldsValid(data)==True):
            data['main_inca'] = same_helper.getMainIncaQhawaxTable(data['qhawax_id'])
            data['installation_date_zone'] = datetime.datetime.now(dateutil.tz.tzutc())
            data['last_time_physically_turn_on_zone'] = datetime.datetime.now(dateutil.tz.tzutc())
            data['last_registration_time_zone'] = datetime.datetime.now(dateutil.tz.tzutc())
            qhawax_installation = QhawaxInstallationHistory(**data)
            session.add(qhawax_installation)
            session.commit()
        else:
            raise Exception("qHAWAX Installation fields have to have data")
    else:
        raise TypeError("The Json company "+str(data)+" should be in Json Format")


def writeBinnacle(qhawax_name,description,person_in_charge):
    """
    Write observations in Binnacle

    """
    if(isinstance(qhawax_name, str) is not True):
        raise TypeError("qHAWAX name should be string")

    if(isinstance(description, str) is not True):
        raise TypeError("Binnacle description should be string")

    if(isinstance(person_in_charge, str) is not True):
        raise TypeError("Person in Charge should be string")

    qhawax_id = same_helper.getQhawaxID(qhawax_name)
    if(qhawax_id is not None):
        bitacora = {'timestamp_zone': datetime.datetime.now(dateutil.tz.tzutc()), \
                    'observation_type': 'Interna','description': description,  \
                    'qhawax_id':qhawax_id,'solution':None,'person_in_charge':person_in_charge, \
                    'end_date_zone':None,'start_date_zone':None}
        bitacora_update = Bitacora(**bitacora)
        session.add(bitacora_update)
        session.commit()
        


