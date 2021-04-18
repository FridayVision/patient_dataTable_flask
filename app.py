import pymongo
from flask import Flask, request, jsonify, render_template, json, redirect
from flask_mongoengine import MongoEngine
from datetime import datetime
import os

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'plb_dev',
    'host': 'localhost',
    'port': 27017
}

#mongodb+srv://:@cluster0.p4u4d.mongodb.net/
#mongodb+srv://drobe444:derin444@cluster0.p4u4d.mongodb.net/plb_dev?retryWrites=true&w=majority
#mongodb+srv://userDb:userDb@cluster0.p4u4d.mongodb.net/plb_dev?retryWrites=true&w=majority

#DB_URI = "mongodb+srv://drobe444:derin444@cluster0.p4u4d.mongodb.net/plb_dev?retryWrites=true&w=majority"
DB_URI = os.environ.get('MONGODB_URI', None)
app.config['MONGODB_SETTINGS'] = {
    'host': os.environ.get('MONGODB_URI', DB_URI)
}
db = MongoEngine()
db.init_app(app)

class patient_col(db.Document):
    Legacy_ID = db.IntField()
    Patient_Name = db.StringField()
    Age = db.StringField()
    Gender = db.StringField()
    Contact_Details = db.StringField()
    Medical_History = db.StringField()
    Investigations_Done = db.StringField()
    Diagnosis = db.StringField()
    Submit_time = db.DateTimeField()

@app.route('/')
def home_page():
    return render_template('form.html')

@app.route('/search')
def query_records():
    employee = patient_col.objects.all()
    return render_template('search3.html', patient=employee)


@app.route('/updatepatient', methods=['POST'])
def updatepatient():
    pk = request.form['pk']
    namepost = request.form['name']
    value = request.form['value']
    patient_update = patient_col.objects(id=pk).first()
    if not patient_update:
        return json.dumps({'error':'data not found'})
    else:
        if namepost == 'Patient_Name':
            patient_update.update(Patient_Name=value)
        elif namepost == 'Age':
            patient_update.update(Age=value)
        elif namepost == 'Gender':
            patient_update.update(Gender=value)
        elif namepost == 'Contact_Details':
            patient_update.update(Contact_Details=value)
        elif namepost == 'Medical_History':
            patient_update.update(Medical_History=value)
        elif namepost == 'Investigations_Done':
            patient_update.update(Investigations_Done=value)
        elif namepost == 'Diagnosis':
            patient_update.update(Diagnosis=value)
    return json.dumps({'status':'OK'})


@app.route('/add', methods=['GET', 'POST'])
def create_record():
    Patient_Name = request.form['Patient_Name']
    Age = request.form['Age']
    Gender = request.form['Gender']
    Contact_Details = request.form['Contact_Details']
    Medical_History = request.form['Medical_History']
    Investigations_Done = request.form['Investigations_Done']
    Diagnosis = request.form['Diagnosis']
    Legacy_ID = findAll()
    patientsave = patient_col(Patient_Name=Patient_Name
                           , Legacy_ID = Legacy_ID
                           , Age=Age
                           , Gender=Gender
                           , Contact_Details=Contact_Details
                           , Medical_History=Medical_History
                           , Investigations_Done=Investigations_Done
                           , Diagnosis=Diagnosis
                           , Submit_time = datetime.now())
    patientsave.save()
    return redirect('/search')

#@app.route('/find', methods=['GET'])
def findAll():
    client = pymongo.MongoClient(DB_URI)
    db1 = client.get_database('plb_dev')
    records = db1.patient_col
    temp = list(records.find().skip(records.count() - 1))
    latest_id = temp[0]['Legacy_ID']
    print("LATEST ID : ",latest_id)
    next_id = int(latest_id) +1
    print("NEXT ID: ",next_id)
    return int(next_id)


@app.route('/delete/<string:getid>', methods=['POST', 'GET'])
def delete_employee(getid):
    print(getid)
    patient_del = patient_col.objects(id=getid).first()
    if not patient_del:
        return jsonify({'error': 'data not found'})
    else:
        patient_del.delete()
    return redirect('/search')



if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
