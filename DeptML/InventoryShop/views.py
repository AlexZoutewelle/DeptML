import os
import pandas as pd
import numpy as np
import sqlite3
import pickle
from tffm import TFFMRegressor
import tensorflow as tf
from django.conf import settings
from django.shortcuts import render
from rest_framework import views
from rest_framework import status
from rest_framework.response import Response
from .models import EmpWithItems
from .models import Employees
from .models import Inventory
from scipy.sparse import csr_matrix

# Create your views here.



#Het volgende is een query naar Inventory, Employees en EmpWithItems, allemaal in 1 keer.



class Train(views.APIView):
    def post(self, request):

                                    #Fetch data from database
        rows_X = []
        ratings_Y = []

        #The following is a query: it selects everything from the EmpWithItems table, along with the Employees and Inventory items, using their foreign keys
        querySet = EmpWithItems.objects.select_related()

        #We split the data into the rows we need. One for X, and one for Y
        for i in querySet:
            rows_X.append([i.Inventory.id, i.Employees.id, i.Employees.Role])
            ratings_Y.append(i.rating)

        #Creating Pandas dataframes
        df_X = pd.DataFrame(rows_X, columns=['InventoryId', 'EmployeeId', 'Role'])
        df_X['InventoryId'] = df_X['InventoryId'].apply(str)
        df_X['EmployeeId'] = df_X['EmployeeId'].apply(str)
        df_X = pd.get_dummies(df_X)
        df_Y = pd.DataFrame(ratings_Y, columns=['Rating'])

        #Sparse matrix for the X, normal array (as matrix) for the Y
        X = csr_matrix(df_X)
        y = np.array(df_Y['Rating'].as_matrix())

        #Instantiation of our model
        model = TFFMRegressor(
            order=8,
            rank=7,
            optimizer=tf.train.GradientDescentOptimizer(learning_rate=0.01),
            n_epochs=15000,
            batch_size=-1,
            init_std=0.01,
            input_type='sparse'
        )

        #Training
        model.fit(X, y, show_progress=True)
        #Save this model in the Models directory
        model.save_state('./Models/RecEngine')


        print("OK")
        return Response(status=status.HTTP_200_OK)



class Predict(views.APIView):
    def post(self, request):
        predictions  = []

        #Instantiate our model
        model = TFFMRegressor(
            order=8,
            rank=7,
            optimizer=tf.train.GradientDescentOptimizer(learning_rate=0.01),
            n_epochs=15000,
            batch_size=-1,
            init_std=0.01,
            input_type='sparse'
        )

        #First, we need to pass it the number of features it's trained on
        model.core.set_num()    #Dit getal moet je nog ff zien te pakken

        #Then, we load it's data from de Models directory
        model.load_state('./Models/RecEngine')

        #Then, we need to query the database for two things:

            #1, the data of this user: Role, etc

            #2, all the inventoryid's we have in the database



        #Lastly, we iterate over all the itemIds to make predictions, and show the user the best ones
        predictions = model.predict()

        return Response(status=status.HTTP_200_OK)


trainClass = Train()
trainClass.post('')

def home(request):
    context = {
    }
    return render(request, 'InventoryShop/home.html', context)   #Tweede parameter: kijkt naar de templates folder -> InventoryShop folder -> pak home.html

