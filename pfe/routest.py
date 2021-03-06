"""Simple travelling salesman problem between cities."""

from __future__ import print_function
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import numpy as np
import mysql.connector
from mysql.connector import Error



def get_coordinates(adress):
    records=[]
    try:
        connection = mysql.connector.connect(host='localhost',
                                         database='optimatets',
                                         user='root',
                                         password='')
        reqet = "SELECT lat,lng FROM places  where city='"+adress+"' AND name='city';"
        cursor = connection.cursor()
        cursor.execute(reqet)
        records.append(cursor.fetchall())
    except Error as e:
        print("Error reading data from MySQL table", e)
    finally:
        if (connection.is_connected()):
            connection.close()
            cursor.close()
            print("MySQL connection is closed")
    
    return(records[0][0])

def fill_cordinates_matrix(adress):
    lat=[]
    lng=[]
    for x in adress:
        lat.append(get_coordinates(adress[x])[0][0])
        lng.append(get_coordinates(adress[x])[0][1])
    return [lat,lng]
        
    
def fill_cordinates(adress):
    corr=[]
    for x in adress:
        corr.append(get_coordinates(adress[x]))
        
    return corr
    
        
def get_matrix_distace(adress):
    from scipy.spatial import distance
    coordinates=fill_cordinates(adress)
    matrix=distance.cdist(coordinates, coordinates, 'euclidean')
    return matrix





#d={'adress0': 'sfax', 'adress1': 'sousse', 'adress2': 'kasserine', 'adress3': 'mahdia', 'adress4': 'medenine', 'adress5': 'gafsa'}




def create_data_model(d):
    """Stores the data for the problem."""
    data = {}
    data['distance_matrix'] =get_matrix_distace(d)  # yapf: disable
    data['num_vehicles'] = 1
    data['depot'] = 0
    data['adress']=list(d.values()) 
    return data


def print_solution(manager, routing, solution,data):
    """Prints solution on console."""
    print('Objective: {} miles'.format(solution.ObjectiveValue()))
    index = routing.Start(0)
    plan_output = 'Route for vehicle 0:\n'
    route_distance = 0
    while not routing.IsEnd(index):
        plan_output += data['adress'][index]+"-->"
        previous_index = index
        index = solution.Value(routing.NextVar(index))
        route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
    plan_output += data['adress'][routing.Start(0)]
    print(plan_output)
    plan_output += 'Route distance: {}miles\n'.format(route_distance)


def get_solution(manager, routing, solution,data):
    """Prints solution on console."""
    
    index = routing.Start(0)
    plan_output = []
    route_distance = 0
    while not routing.IsEnd(index):
        plan_output.append({'adress':data['adress'][index],'cord':get_coordinates(data['adress'][index])})
        previous_index = index
        index = solution.Value(routing.NextVar(index))
        route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
    plan_output.append({'adress':data['adress'][routing.Start(0)]})
    print(plan_output)
    return plan_output




def main(d):
    """Entry point of the program."""
    # Instantiate the data problem.
    data = create_data_model(d)

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                           data['num_vehicles'], data['depot'])

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)


    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if solution:
        print_solution(manager, routing, solution,data)
        result=get_solution(manager, routing, solution,data)
    return result

from flask import Flask, request, make_response
import json
app = Flask(__name__)
@app.route('/', methods=['POST'])


def index():
    
    d = request.form.to_dict() # data recived from form
   
    data=make_response(json.dumps(main(d))) # transform final result to json
    resp=data
    resp.status_code = 200
    resp.headers['Access-Control-Allow-Origin'] = '*' # configiration 
 
    return resp

if __name__ == '__main__':
    app.run()
    


