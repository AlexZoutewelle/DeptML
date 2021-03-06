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
def TrainModel():
                                #Fetch data from database
    rows_X = []
    ratings_Y = []

    #The following is a query: it selects everything from the EmpWithItems table, along with the Employees and Inventory items, using their foreign keys
    querySet = EmpWithItems.objects.select_related()
    for i in querySet:
        print(i)

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
    print("Shape of df_X: "  + str(df_X.shape))
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

def CreatePredictor():
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

    # Then, for input, we unpickle the empty row we saved during training
    inputRow = pd.read_pickle("./Models/InputRowX")
    print("shape of inputRowX: " + str(inputRow.shape[1]))

    print("Model created. Setting number of features...")
    # First, we need to pass it the number of features it's trained on
    model.core.set_num_features(inputRow.shape[1])

    print("Loading previous model state..")
    # Then, we load it's data from de Models directory
    model.load_state('./Models/RecEngine')

    return [model, inputRow]

class Predict(views.APIView):
    def post(self, request, employeeIdd, employeeRolee):
        print("start")


                            # # Then, for input, we unpickle the empty row we saved during training
                            # inputRow = pd.read_pickle("./Models/InputRowX")
                            # print("shape of inputRowX: " + str(inputRow.shape[1]))

                            # To ready this input row, we first need the users' Id and Function Role

        model = modelInstantiation[0]
        inputRow = modelInstantiation[1]

        employeeId = employeeIdd
        employeeRole = employeeRolee

        print("shape of inputRowX: " + str(inputRow.shape[1]))

        # We insert those values in their correspondent columns
        inputRow['EmployeeId_' + str(employeeId)] = 1
        inputRow['Role_' + str(employeeRole)] = 1

        print("shape of inputRowX: " + str(inputRow.shape[1]))
        # Lastly, we iterate over all the itemIds to make predictions, and show the user the best ones

        # Query for all Ids, these must be unique
        querySet = EmpWithItems.objects.select_related('Inventory')
        print("the QuerySet: ")
        print(querySet)
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


                            # print("Creating model..")

                            # # Instantiate our model
                            # model = TFFMRegressor(
                            #     order=8,
                            #     rank=7,
                            #     optimizer=tf.train.GradientDescentOptimizer(learning_rate=0.01),
                            #     n_epochs=15000,
                            #     batch_size=-1,
                            #     init_std=0.01,
                            #     input_type='sparse'
                            # )
                            #
                            # print("Model created. Setting number of features...")
                            # # First, we need to pass it the number of features it's trained on
                            # model.core.set_num_features(inputMatrix.shape[1])
                            # print(inputMatrix.shape[1])
                            # print("Loading previous model state..")
                            # # Then, we load it's data from de Models directory
                            # model.load_state('./Models/RecEngine')


        print("Starting prediction..")

        x = csr_matrix(inputMatrix)

        predictions = model.predict(x)

        #Now that we have our predictions, we need to create a tuple of {InventoryId, predictedRating}

        #Create the list for the predictions
        predictions_List = []

        print("Predictions done!")
        for i in predictions:
            predictions_List.append(i)


        for i in predictions_List:
            print(i)

        #Create a list of tuples
        tuple_list = zip(InventoryIds, predictions_List)
        #Select the 10 highest rated items
        tuple_list = sorted(tuple_list, key=lambda x: x[1], reverse=True)

        ChosenItems = []
        print("Created tuples")
        for i in range(10):
            print(tuple_list[i])
            ChosenItems.append(Inventory.objects.get(pk=tuple_list[i][0]))

        print("End!")

        return ChosenItems
        #return Response(status=status.HTTP_200_OK)
#trainClass = Predict()
#trainClass.post('')
modelInstantiation = CreatePredictor()
allProducts = Inventory.objects.all()

def home(request, employeeIdd=11798, employeeRolee='Full-stack Developer'):
    trainClass = Predict()
    recommendedItems = trainClass.post('', employeeIdd, employeeRolee)
    context = {
        'inventory': recommendedItems,
    }
    return render(request, 'InventoryShop/home.html', context)   #Tweede parameter: kijkt naar de templates folder -> InventoryShop folder -> pak home.html


def iosdeveloper(request, employeeIdd=15219, employeeRolee='ios developer'):
    trainClass = Predict()
    recommendedItems = trainClass.post('', employeeIdd, employeeRolee)
    context = {
        'inventory': recommendedItems,
    }
    return render(request, 'InventoryShop/home.html', context)


def datascientist(request, employeeIdd=6267, employeeRolee='Data Scientist'):
    trainClass = Predict()
    recommendedItems = trainClass.post('', employeeIdd, employeeRolee)
    context = {
        'inventory': recommendedItems,
    }
    return render(request, 'InventoryShop/home.html', context)

def softwaretester(request, employeeIdd=11800, employeeRolee='Software tester'):
    trainClass = Predict()
    recommendedItems = trainClass.post('', employeeIdd, employeeRolee)
    context = {
        'inventory': recommendedItems,
    }
    return render(request, 'InventoryShop/home.html', context)
    #15219 = ios developer
    #11798 = fullstack
    #6267 = data scientist
    #11800 = software tester