# -*- coding:utf-8 -*-

import csv
import os
import sys
c=5
longtern=30
shortern=10
list_longtern=[]
list_shortern=[]
meanline_longtern=0
meanline_shortern=0
count_longtern=0
full_longtern=0
count_shortern=0
full_shortern=0
gold_cross=0
gap=0
gap_to_buy=100
status=0
action=0
money=0
last_day=0
last_buy_price=0
def calculate_longtern():
    global meanline_longtern,list_longtern
    meanline_longtern=0
    for item in list_longtern:
        meanline_longtern+=float(item)
    meanline_longtern=meanline_longtern/longtern	#算出長期均線
    return meanline_longtern
def calculate_shortern():
    global meanline_shortern,list_shortern
    meanline_shortern=0
    for item in list_shortern:
        meanline_shortern+=float(item)
    meanline_shortern=meanline_shortern/shortern	#算出長期均線
    return meanline_shortern
def predict_action(row):
    global meanline_longtern,meanline_shortern,count_longtern,count_shortern
    global list_longtern,list_shortern,full_longtern,full_shortern
    a=row[0]
    d=row[3]
    action2=0
    if(full_longtern==0):
        list_longtern.append(a)
        count_longtern+=1
        if(count_longtern==longtern):
            full_longtern=1
            count_longtern=0
    elif full_longtern == 1:
        del list_longtern[count_longtern]
        list_longtern.insert(count_longtern,a)
        count_longtern+=1
        if count_longtern==longtern:
            count_longtern=0
    if full_shortern==0:
        list_shortern.append(a)
        count_shortern+=1
        if(count_shortern==shortern):
            full_shortern=1
            count_shortern=0
    elif full_shortern == 1:
        del list_shortern[count_shortern]
        list_shortern.insert(count_shortern,a)
        count_shortern+=1
        if count_shortern==shortern:
            count_shortern=0
    if (full_shortern==1 and full_longtern==1):
        action2=buy_or_not(a,d)
    return str(action2)
def buy_or_not(a,d):
    global meanline_longtern,meanline_shortern,count_longtern,count_shortern
    global list_longtern,list_shortern,full_longtern,full_shortern,gold_cross,gap
    global action,money
    action2=0
    do_action(a,d)
    if(calculate_longtern()>=calculate_shortern()):
        if(gold_cross==1 and gap>=gap_to_buy):
            print("售出")
            if(status==1 and float(d)>=last_buy_price):
                action=-1
                action2=-1
            elif(status==0):
                action=-1
                action2=-1
            gold_cross=0
            gap=calculate_shortern()-calculate_longtern()
        elif(gold_cross==1):
            gold_cross=0
            gap=calculate_shortern()-calculate_longtern()
        elif(gold_cross==0):
            gap+=(calculate_shortern()-calculate_longtern())
        print(str(gold_cross)+"  60ma="+str(calculate_longtern())+"\t20ma="+str(calculate_shortern())+"\tprice="+a+"  gap="+str(int(gap))+"\tmoney="+str(money))
    if(calculate_longtern()<=calculate_shortern()):
        if(gold_cross==0 and gap<=-gap_to_buy):
            print("買入")
            if(status==-1 and float(d)<=last_buy_price):
                action=1
                action2=1
            elif(status==0):
                action=1
                action2=1
            gold_cross=1
            gap=calculate_shortern()-calculate_longtern()
        elif(gold_cross==0):
            gold_cross=1
            gap=calculate_shortern()-calculate_longtern()
        elif(gold_cross==1):
            gap+=(calculate_shortern()-calculate_longtern())
        print(str(gold_cross)+"  60ma="+str(calculate_longtern())+"\t20ma="+str(calculate_shortern())+"\tprice="+a+"\tgap="+str(int(gap))+"\tmoney="+str(money))
    return action2
def do_action(a,d):
    global action,status,money,last_buy_price
    if action==1:
        if(status==-1):
            status=0
            action=0
            money-=float(a)
        elif status==0:
            status=1
            action=0
            money-=float(a)
            last_buy_price=float(a)
        elif status==1:
            action=0
    elif action==-1:
        if(status==-1):
            action=0
        elif status==0:
            status=-1
            action=0
            money+=float(a)
            last_buy_price=float(a)
        elif status==1:
            status=0
            action=0
            money+=float(a)
# You can write code above the if-main block.
if __name__ == '__main__':
    # You should not modify this part.
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--training',
                       default='training_data.csv',
                       help='input training data file name')
    parser.add_argument('--testing',
                        default='testing_data.csv',
                        help='input testing data file name')
    parser.add_argument('--output',
                        default='output.csv',
                        help='output file name')
    args = parser.parse_args()

    #global last_day
    file = open(args.testing, 'r')
    csvCursor = csv.reader(file)
    file2 = open(args.output, 'w')
    csvCursor2 = csv.writer(file2)
    
    #print(csvCursor)
    openprice = []
    
    for row in csvCursor:
        openprice.append(row)

    file.close()
    #money-=float(openprice[0][0])
    last_buy_price=float(openprice[0][0])
    first_row=0
    for row in openprice:
        #print (row[0])
        if(first_row==1):
            if(action==0):
                csvCursor2.writerow("0")
            elif(action==1):
                csvCursor2.writerow("1")
            elif(action==-1):
                csvCursor2.writerow(["-1"])
        first_row=1
        last_day=row[0]
        action2=predict_action(row)

    print ("status:"+str(status))
    if(status==0):
        print("money="+str(money))
    elif status==1:
        status=0
        money+=float(last_day)
        print("money="+str(money))
    elif status==-1:
        status=0
        money-=float(last_day)
        print("money="+str(money))
    

    '''
    # The following part is an example.
    # You can modify it at will.
    training_data = load_data(args.training)
    trader = Trader()
    trader.train(training_data)
    
    testing_data = load_data(args.testing)
    with open(args.output, 'w') as output_file:
        for row in testing_data:
            # We will perform your action as the open price in the next day.
            action = trader.predict_action(datum)
            output_file.write(action)

            # this is your option, you can leave it empty.
            trader.re_training(i)
    '''
