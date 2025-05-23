###### Your ID ######
# ID1: 318974730 Yarin Twito
# ID2: 207251497 Nadav Passal
#####################

# imports 
import numpy as np
import pandas as pd

def preprocess(X,y):
    """
    Perform Standardization on the features and true labels.

    Input:
    - X: Input data (m instances over n features).
    - y: True labels (m instances).

    Returns:
    - X: The Standardized input data.
    - y: The Standardized true labels.
    """
    ###########################################################################
    # TODO: Implement the normalization function.                             #
    ###########################################################################
    avg_x = np.mean(X, axis=0)
    std_dev_x = np.std(X, axis=0)

    X = (X - avg_x) / std_dev_x

    avg_y = np.mean(y)
    std_dev_y = np.std(y)

    y = (y - avg_y) / std_dev_y
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    return X, y

def apply_bias_trick(X):
    """
    Applies the bias trick to the input data.

    Input:
    - X: Input data (n instances over p features).

    Returns:
    - X: Input data with an additional column of ones in the
        zeroth position (n instances over p+1).
    """
    ###########################################################################
    # TODO: Implement the bias trick by adding a column of ones to the data.                             #
    ###########################################################################
    ones = np.ones(X.shape[0])
    X = np.column_stack((ones,X))
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    return X

def compute_loss(X, y, theta):
    """
    Computes the average squared difference between an observation's actual and
    predicted values for linear regression.  

    Input:
    - X: Input data (n instances over p features).
    - y: True labels (n instances).
    - theta: the parameters (weights) of the model being learned.

    Returns:
    - J: the loss associated with the current set of parameters (single number).
    """
    
    J = 0  # We use J for the loss.
    ###########################################################################
    # TODO: Implement the MSE loss function.                                  #
    ###########################################################################
    prediction = np.dot(X,theta)
    error = prediction - y

    J = np.mean(np.square(error)) / 2
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    return J

def gradient_descent(X, y, theta, eta, num_iters):
    """
    Learn the parameters of the model using gradient descent using 
    the training set. Gradient descent is an optimization algorithm 
    used to minimize some (loss) function by iteratively moving in 
    the direction of steepest descent as defined by the negative of 
    the gradient. We use gradient descent to update the parameters
    (weights) of our model.

    Input:
    - X: Input data (n instances over p features).
    - y: True labels (n instances).
    - theta: The parameters (weights) of the model being learned.
    - eta: The learning rate of your model.
    - num_iters: The number of updates performed.

    Returns:
    - theta: The learned parameters of your model.
    - J_history: the loss value for every iteration.
    """
    
    theta = theta.copy() # optional: theta outside the function will not change
    J_history = [] # Use a python list to save the loss value in every iteration
    ###########################################################################
    # TODO: Implement the gradient descent optimization algorithm.            #
    ###########################################################################
    m = X.shape[0]
    for i in range(num_iters):
        mult = np.dot(X,theta)
        inner = mult - y
        loss_value = compute_loss(X,y,theta)
        J_history.append(loss_value)

        theta = theta - (eta / m) * np.dot(X.T, inner)
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    return theta, J_history

def compute_pinv(X, y):
    """
    Compute the optimal values of the parameters using the pseudoinverse
    approach as you saw in class using the training set.

    #########################################
    #### Note: DO NOT USE np.linalg.pinv ####
    #########################################

    Input:
    - X: Input data (n instances over p features).
    - y: True labels (n instances).

    Returns:
    - pinv_theta: The optimal parameters of your model.
    """
    
    pinv_theta = []
    ###########################################################################
    # TODO: Implement the pseudoinverse algorithm.                            #
    ###########################################################################
    mult = np.matmul(X.T,X)
    inv = np.linalg.inv(mult)
    pinv = np.matmul(inv,X.T)
    pinv_theta = np.matmul(pinv,y)
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    return pinv_theta

def gradient_descent_stop_condition(X, y, theta, eta, max_iter, epsilon=1e-8):
    """
    Learn the parameters of your model using the training set, but stop 
    the learning process once the improvement of the loss value is smaller 
    than epsilon. This function is very similar to the gradient descent 
    function you already implemented.

    Input:
    - X: Input data (n instances over p features).
    - y: True labels (n instances).
    - theta: The parameters (weights) of the model being learned.
    - eta: The learning rate of your model.
    - max_iter: The maximum number of iterations.
    - epsilon: The threshold for the improvement of the loss value.
    Returns:
    - theta: The learned parameters of your model.
    - J_history: the loss value for every iteration.
    """
    
    theta = theta.copy() # optional: theta outside the function will not change
    J_history = [] # Use a python list to save the loss value in every iteration
    ###########################################################################
    # TODO: Implement the gradient descent with stop condition optimization algorithm.  #
    ###########################################################################
    m = X.shape[0]
    for i in range(max_iter):
        mult = np.dot(X,theta)
        inner = mult - y
        theta = theta - (eta / m) * np.dot(X.T, inner)
        loss_value = compute_loss(X,y,theta)
        J_history.append(loss_value)
        if len(J_history) >= 2 and (J_history[-2] - J_history[-1] ) < epsilon:
            break
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    return theta, J_history

def find_best_learning_rate(X_train, y_train, X_val, y_val, iterations):
    """
    Iterate over the provided values of eta and train a model using 
    the training dataset. Maintain a python dictionary with eta as the 
    key and the loss on the validation set as the value.

    You should use the efficient version of gradient descent for this part. 

    Input:
    - X_train, y_train, X_val, y_val: the training and validation data
    - iterations: maximum number of iterations

    Returns:
    - eta_dict: A python dictionary - {eta_value : validation_loss}
    """
    
    etas = [0.00001, 0.00003, 0.0001, 0.0003, 0.001, 0.003, 0.01, 0.03, 0.1, 0.3, 1, 2, 3]
    eta_dict = {} # {eta_value: validation_loss}
    ###########################################################################
    # TODO: Implement the function and find the best eta value.             #
    ###########################################################################
    m = X_train.shape[1] 
    np.random.seed(42)
    random_theta = np.random.random(m)
    for eta in etas:
        theta, _ = gradient_descent(X_train,y_train,random_theta,eta,iterations)
        loss = compute_loss(X_val,y_val,theta)
        eta_dict[eta] =  loss

    
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    return eta_dict

def forward_feature_selection(X_train, y_train, X_val, y_val, best_eta, iterations):
    """
    Forward feature selection is a greedy, iterative algorithm used to 
    select the most relevant features for a predictive model. The objective 
    of this algorithm is to improve the model's performance by identifying 
    and using only the most relevant features, potentially reducing overfitting, 
    improving accuracy, and reducing computational cost.

    You should use the efficient version of gradient descent for this part. 

    Input:
    - X_train, y_train, X_val, y_val: the input data without bias trick
    - best_eta: the best learning rate previously obtained
    - iterations: maximum number of iterations for gradient descent

    Returns:
    - selected_features: A list of selected top 5 feature indices
    """
    selected_features = []
    #####c######################################################################
    # TODO: Implement the function and find the best eta value.             #
    ###########################################################################
    new_feature = None
    best_loss = float('inf')
    num_features = X_train.shape[1]
    for _ in range(5):
        for i in range(num_features):
            if i in selected_features:
                continue
            
            curr = selected_features + [i]

            sub_train = X_train[:,curr]
            sub_val = X_val[:, curr]

            bias_val = apply_bias_trick(sub_val)
            bias_train = apply_bias_trick(sub_train)


            base_theta = np.zeros(bias_train.shape[1])
            theta, _ = gradient_descent_stop_condition(bias_train,y_train,base_theta,best_eta,iterations)
            curr_loss = compute_loss(bias_val,y_val,theta)

            if curr_loss < best_loss:
                new_feature = i
                best_loss = curr_loss

        selected_features.append(new_feature)

    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    return selected_features

def create_square_features(df):
    """
    Create square features for the input data.

    Input:
    - df: Input data (n instances over p features) as a dataframe.

    Returns:
    - df_poly: The input data with polynomial features added as a dataframe
               with appropriate feature names
    """

    df_poly = df.copy()
    ###########################################################################
    # TODO: Implement the function to add polynomial features                 #
    ###########################################################################
    squared = {}
    for col in df_poly.columns:
        col_name = f"{col}^2"
        new_col =  np.square(df_poly[col])

        squared[col_name] = new_col
    cols = df_poly.columns.tolist()

    mult = {}

    for i in range(len(cols)):
        for j in range(i + 1, len(cols)):
            col_name = f"{cols[i]} * {cols[j]}"

            new_col = df_poly[cols[i]] * df_poly[cols[j]]

            mult[col_name] = new_col
    
    mult_df = pd.DataFrame(mult)
    squared_df = pd.DataFrame(squared)

    df_poly = pd.concat([mult_df,squared_df,df],axis=1)
    
    
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    return df_poly