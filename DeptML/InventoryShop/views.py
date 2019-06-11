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
from django.shortcuts import HttpResponse


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

        #Before we train, we pickle an empty row from the dataframe, so we can use it later in prediction tasks
        df_copy = pd.DataFrame(0, [1], columns=df_X.columns)
        print("Shape of df_X: "  + str(df_X.shape[1]))
        df_copy.to_pickle("./Models/InputRowX")


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
        model.destroy()
        return Response(status=status.HTTP_200_OK)



class Predict(views.APIView):
    def post(self, request):

        print("start")
        # Then, for input, we unpickle the empty row we saved during training
        inputRow = pd.read_pickle("./Models/InputRowX")
        print("shape of inputRowX: " + str(inputRow.shape[1]))

        # To ready this input row, we first need the users' Id and Function Role
        employeeId = 10436
        employeeRole = "Front-end Developer"

        print("shape of inputRowX: " + str(inputRow.shape[1]))

        # We insert those values in their correspondent columns
        inputRow['EmployeeId_' + str(employeeId)] = 1
        inputRow['Role_' + str(employeeRole)] = 1

        print("shape of inputRowX: " + str(inputRow.shape[1]))


        # Lastly, we iterate over all the itemIds to make predictions, and show the user the best ones

        # Query for all Ids, these must be unique
        querySet = EmpWithItems.objects.select_related()
        InventoryIds = []
        for i in querySet:
            if i.Inventory.id not in InventoryIds:
                InventoryIds.append(i.Inventory.id)
                print(str(i.Inventory.id))


        # For each Id, we need a new row, effectively creating a matrix
        inputMatrix = pd.concat([inputRow] * len(InventoryIds), ignore_index=True)
        print("shape of inputRowX: " + str(inputMatrix.shape[1]))

        print("Columns: " + inputMatrix.columns)
        # For each Id, we put it in the input row
        for i in range(len(InventoryIds)):
            currentColumn = "InventoryId_" + str(InventoryIds[i])
            inputMatrix.at[i, currentColumn] = 1
            print(currentColumn)


        print("Creating model..")

        # Instantiate our model
        model = TFFMRegressor(
            order=8,
            rank=7,
            optimizer=tf.train.GradientDescentOptimizer(learning_rate=0.01),
            n_epochs=15000,
            batch_size=-1,
            init_std=0.01,
            input_type='sparse'
        )

        print("Model created. Setting number of features...")
        # First, we need to pass it the number of features it's trained on
        model.core.set_num_features(inputMatrix.shape[1])    #Dit getal moet je nog ff zien te pakken
        print(inputMatrix.shape[1])
        print("Loading previous model state..")
        # Then, we load it's data from de Models directory
        model.load_state('./Models/RecEngine')


        print("Starting prediction..")

        x = csr_matrix(inputMatrix)

        predictions = model.predict(x)

        print("Predictions done!")
        for i in predictions:
            print(i)

        print("End!")
        return Response(status=status.HTTP_200_OK)


trainClass = Predict()
trainClass.post('')


allProducts = Inventory.objects.all()

def home(request):
    context = {
        'inventory' : allProducts,
    }
    return render(request, 'InventoryShop/home.html', context)   #Tweede parameter: kijkt naar de templates folder -> InventoryShop folder -> pak home.html

