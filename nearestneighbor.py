import sys
import copy
import math
from math import floor
from sys import maxsize

#---Nearest Neighbor function------------
def nearest_neighbor(data, row_to_skip, test_features, features, instances):
  nearest_neighbor = 0
  closest_dist = maxsize

  for i in range(instances): #go through each row
    if row_to_skip == i: #if row to skip? do nothing.
      continue
    else:
      current_distance = 0 #temp distance
      for j in range(len(test_features)): #length of feature subset to test
        #euclidean distance formula
        current_distance = current_distance + pow((data[i][test_features[j]] - data[row_to_skip][test_features[j]]), 2)

      current_distance = math.sqrt(current_distance)

      if current_distance < closest_dist: #nearest so far! set the values
        nearest_neighbor = i #row = the closest instance
        closest_dist = current_distance #new shortest distance

  return nearest_neighbor
#--------------------------

#---Default Evaluation function----
def default_evaluation_function(data, features, instances):
  #Simply returns the odds of the most likely choice of the two classes.
  class_one_hits = 0
  class_two_hits = 0
  for i in range(instances):
    if data[i][0] == 1:
      class_one_hits += 1
    else:
      class_two_hits += 1

  if class_one_hits > class_two_hits:
    accuracy = (class_one_hits / instances) * 100.0
  else:
    accuracy = (class_two_hits / instances) * 100.0

  return accuracy
#--------------------------

#---Evaluation function----
def evaluation_function(data, test_features, features, instances):
  hits = 0.0 #declare the number of hits as a float
  for i in range(instances):
    row_to_skip = i #iterate on which row to skip
    prediction = nearest_neighbor(data, row_to_skip, test_features, features, instances)

    if data[prediction][0] == data[row_to_skip][0]: #check if the prediction matches the actual value
      hits += 1 #increment hits

  accuracy = (hits / instances) * 100.0 #accuracy formula
  return accuracy
#--------------------------

#----Forward selection-----
def forward_selection(data, features, instances): #current forward selection search  uses the given number of features and uses the random evauluation function
  best_accuracy = 0 #save the highest accuracy
  best_features = [] #save the best combination of features
  current_saved_features = [] #hold the current saved features
  immediate_features = [] #hold the features we are testing immediately

  for i in range(1, features + 1): #so 1 - 4 in the simple case
    new_feature = 0 #default
    temp_best_accuracy = 0 #hold the temp best accuracy

    for j in range(1, features + 1):
      if j in current_saved_features: #don't consider a feature we already have 
        continue

      immediate_features = [] #clear
      immediate_features = list(current_saved_features) + [j] #display new feature at the end since appending later
      accuracy = evaluation_function(data, immediate_features, features, instances)
      print("Using feature(s) " + str(immediate_features) + " accuracy is " + str(accuracy) + "%")

      if accuracy > temp_best_accuracy:
        temp_best_accuracy = accuracy
        new_feature = j #save the best feature to append


    current_saved_features.append(new_feature)

    if temp_best_accuracy > best_accuracy:
      best_accuracy = temp_best_accuracy
      best_features = [] #clear
      best_features = list(current_saved_features)
      print("\nFeature set " + str(current_saved_features) + " was best, accuracy is " + str(temp_best_accuracy) + "%\n")

    else:
      print("\n(Warning, Accuracy has decreased! Continuing search in case of local maxima)")
      print("Feature set " + str(current_saved_features) + " was best, accuracy is " + str(temp_best_accuracy) + "%\n")

  print("Finished search!! The best feature subset is "+ str(best_features) + ", which has an accuracy of " + str(floor(best_accuracy*10)/10) + "%\n")
#--------------------------

#---Backward elmination----
def backward_elimination(data, features, instances): #current backward elimination search simply uses the given number of features and uses the random evauluation function - acts somewhat as a mirror of forward selection
  best_accuracy = 0 #save the highest accuracy
  best_features = [] #save the best combination of features
  current_saved_features = list(range(1, features + 1)) #hold the current saved features - initialize to be the full set and keep removing
  immediate_features = [] #hold the features we are testing immediately

  for i in range(1, features + 1): #so 1 - 4 in the simple case
    delete_feature = 0 #default
    temp_best_accuracy = 0 #hold the temp best accuracy

    for j in range(1, features + 1):
      if j not in current_saved_features: #don't consider a feature we already removed
        continue

      immediate_features = copy.deepcopy(current_saved_features) #copy the current features
      immediate_features.remove(j)
      accuracy = evaluation_function(data, immediate_features, features, instances)
      print("Using feature(s) " + str(immediate_features) + " accuracy is " + str(accuracy) + "%")

      if accuracy > temp_best_accuracy:
        temp_best_accuracy = accuracy
        delete_feature = j #save the best feature to delete


    current_saved_features.remove(delete_feature)

    if temp_best_accuracy > best_accuracy:
      best_accuracy = temp_best_accuracy
      best_features = [] #clear
      best_features = list(current_saved_features)
      print("\nFeature set " + str(current_saved_features) + " was best, accuracy is " + str(temp_best_accuracy) + "%\n")

    else:
      print("\n(Warning, Accuracy has decreased! Continuing search in case of local maxima)")
      print("Feature set " + str(current_saved_features) + " was best, accuracy is " + str(temp_best_accuracy) + "%\n")

  print("Finished search!! The best feature subset is "+ str(best_features) + ", which has an accuracy of " + str(floor(best_accuracy*10)/10) + "%\n")
#--------------------------
