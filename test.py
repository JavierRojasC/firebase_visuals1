import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import datetime as dt
import numpy as np

cred = credentials.Certificate("serviceAccountKey2.json")
firebase_admin.initialize_app(cred)

db=firestore.client()
dt_initial = dt.datetime(2022, 8, 16, 6, 0, 0)
dt_final = dt.datetime(2022, 8, 16, 7, 0, 0)


def crear_histograma(db):
    dt_initial = dt.datetime(2022, 8, 17, 6, 0, 0)
    dt_initialString = dt.datetime.strftime(dt_initial, '%Y-%m-%d %H:%M:%S')

    dt_final = dt.datetime(2022, 8, 17, 18, 0, 0)
    dt_finalString = dt.datetime.strftime(dt_final, '%Y-%m-%d %H:%M:%S')

    result = db.collection('sensorTemperatura').where('hora', u'>', dt_initialString).where('hora', u'<', dt_finalString).get()

    values=[]
    for doc in result:
        values.append(doc.to_dict()['temperatura'])
       # print(doc.to_dict())

    hist=np.histogram(values)
    print(values)
    Ejex=hist[1].tolist()
    Ejey=hist[0].tolist()

    print(Ejey)

    #fecha= dt.datetime.now().date().strftime('%Y-%m-%d')
    fecha = "2022-08-17"

    date = dt.datetime.strptime(fecha, '%Y-%m-%d')

    date_clean = date.strftime('%Y%m%d')
    USL=185
    LSL=175
    USL_cant = (USL - np.mean(values)) / (3 * np.std(values))
    LSL_cant = (np.mean(values) - LSL) / (3 * np.std(values))
    cpk_value = min(USL_cant, LSL_cant)


    histograma = {
    u'ejex': Ejex,
    u'ejey': Ejey,
    u'fecha': fecha,
    u'cpk': cpk_value
}

    db.collection(u'estadistica/temperatura/visualesdiarios').document(date_clean).set(histograma)


def growth(initial_date,db):
    dt_final = dt_initial+dt.timedelta(hours=1,minutes=0,seconds=0)
    dt_pre_initial=dt_initial-dt.timedelta(hours=1,minutes=0,seconds=0)
    result_current = db.collection('temperatura').where('date', u'>', dt_initial).where('date', u'<', dt_final).get()
    result_past = db.collection('temperatura').where('date', u'>', dt_pre_initial).where('date', u'<', dt_initial).get()

    values_current=[]
    values_past=[]
    for doc in result_current:
        values_current.append(doc.to_dict()['temp'])
               # print(doc.to_dict())
    for doc in result_past:
        values_past.append(doc.to_dict()['temp'])
               # print(doc.to_dict())

    print(((np.mean(values_current)-np.mean(values_past))/np.mean(values_past))*100)

#OUTPUTS

crear_histograma(db)
#crear_cpk(db)

#se puede implementar en un area chart de la sig manera
# stroke: {
#   curve: 'stepline',
# }


# growth(dt_initial,db)

# cpk(3,0.1,dt_initial,db)
