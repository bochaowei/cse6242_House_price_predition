import project as model_firsttime
import project_new as model
import realtor_scraping as web
import csv
from flask import Flask, render_template, send_from_directory, request
import locale
app = Flask(__name__, static_url_path='')

firstTime = True

@app.route('/', methods=['GET', 'POST'])
def index():
    global firstTime
    if firstTime:
        print(model_firsttime.main())
        firstTime = False
    return render_template('index.html')

@app.route('/result', methods=['GET', 'POST'])
def result():
    if request.method ==  'POST':
        user_in = request.form.to_dict()
    elif request.method ==  'GET':
        user_in = request.args.to_dict()
    soldprice,recomprice=prediction(user_in)
    return render_template('result.html',soldprice=soldprice,recomprice=recomprice)

@app.route('/assets/<path:path>')
def send_assets(path):
    return send_from_directory('assets',path)

@app.route('/data/web/<path:path>')
def send_web(path):
    return send_from_directory('data/web',path)



def prediction(info):
    city=info['city']
    state=info['state']
    del info['city']
    del info['state']
    reader = csv.reader(open('./data/test_default.csv',mode='r'))
    result = {}
    r=0
    mydict={}
    for row in reader:
        result[r]=row
        r=r+1
    for i in range(len(result[0])):
        mydict[result[0][i]]=result[1][i]

    for key in info.keys():
        if info[key]:
            mydict[key]=info[key]

    with open('./data/test.csv', mode='w',newline='') as employee_file:
        employee_writer = csv.writer(employee_file,delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        employee_writer.writerow(mydict.keys())
        employee_writer.writerow(mydict.values())
    model_price=model.main('./data/test.csv')
    print(model_price)
    model_median=model.get_median()
    webresult=web.web_scraper(city,state)
    median_now=webresult[2]
    median_now=float(median_now)*1000
    predict_price=model_price*median_now/model_median
    print('The predicted price for your house is',predict_price)
    median_list=webresult[0]
    median_list=float(median_list)*1000
    recom_price=predict_price*median_list/median_now
    ##improvement suggestion and prediction
    overall_condition=range(1,10)
    mydict_con=mydict.copy()
    with open('./data/web/OverallCond.csv', mode='w',newline='') as myfile:
        myfile.write('overall_condition,predicted_price\n')
        writer = csv.writer(myfile)
        for con in overall_condition:
            mydict_con['OverallCond']=con
            temp_filename='./data/testcond'+str(con)+'.csv'
            with open(temp_filename, mode='w',newline='') as employee_file:
                employee_writer = csv.writer(employee_file,delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                employee_writer.writerow(mydict_con.keys())
                employee_writer.writerow(mydict_con.values())
            model_price_cond=model.main(temp_filename)
            predict_price_cond=model_price_cond*median_now/model_median
            myfile_output=[con,predict_price_cond[0]]
            writer.writerow(myfile_output)
        
    monthsold=range(1,13)
    mydict_month=mydict.copy()
    with open('./data/web/MoSold.csv', mode='w',newline='') as myfile:
        myfile.write('Month_Sold,predicted_price\n')
        writer = csv.writer(myfile)
        for month in monthsold:
            mydict_month['MoSold']=month
            temp_filename='./data/testmonth'+str(month)+'.csv'
            with open(temp_filename, mode='w',newline='') as employee_file:
                employee_writer = csv.writer(employee_file,delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                employee_writer.writerow(mydict_month.keys())
                employee_writer.writerow(mydict_month.values())
            model_price_cond=model.main(temp_filename)
            predict_price_cond=model_price_cond*median_now/model_median
            myfile_output=[month,predict_price_cond[0]]
            writer.writerow(myfile_output)
            
    Neighborhood=['Crawfor','NridgHt','Mitchel','OldTown']
    mydict_nei=mydict.copy()
    with open('./data/web/Neighborhood.csv', mode='w',newline='') as myfile:
        myfile.write('Neighborhood,predicted_price\n')
        writer = csv.writer(myfile)
        for nei in Neighborhood:
            mydict_nei['Neighborhood']=nei
            temp_filename='./data/testnei'+str(nei)+'.csv'
            with open(temp_filename, mode='w',newline='') as employee_file:
                employee_writer = csv.writer(employee_file,delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                employee_writer.writerow(mydict_nei.keys())
                employee_writer.writerow(mydict_nei.values())
            model_price_cond=model.main(temp_filename)
            predict_price_cond=model_price_cond*median_now/model_median
            myfile_output=[nei,predict_price_cond[0]]
            writer.writerow(myfile_output)
            
    KitchenQual=['Ex','Gd','Fa','TA']
    mydict_kit=mydict.copy()
    with open('./data/web/KitchenQual.csv', mode='w',newline='') as myfile:
        myfile.write('Kitchen_Quality,predicted_price\n')
        writer = csv.writer(myfile)
        for kit in KitchenQual:
            mydict_kit['KitchenQual']=kit
            temp_filename='./data/testkit'+str(kit)+'.csv'
            with open(temp_filename, mode='w',newline='') as employee_file:
                employee_writer = csv.writer(employee_file,delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                employee_writer.writerow(mydict_kit.keys())
                employee_writer.writerow(mydict_kit.values())
            model_price_cond=model.main(temp_filename)
            predict_price_cond=model_price_cond*median_now/model_median
            myfile_output=[kit,predict_price_cond[0]]
            writer.writerow(myfile_output)    
            
    locale.setlocale(locale.LC_ALL, 'en_US')
    predict_price=locale.format_string("%d", round(predict_price[0]), grouping=True)
    recom_price=locale.format_string("%d", round(recom_price[0]), grouping=True)
    return predict_price,recom_price

if __name__ == '__main__':
    app.run(debug=True)
