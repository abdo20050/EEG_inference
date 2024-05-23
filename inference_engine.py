from sklearn.preprocessing import StandardScaler
import numpy as np
import tensorflow as tf
import robot.BothHands_action
import robot.LeftHand_action
import robot.RightHand_action
# model__subject-1_05_13_13_46
# model_path = './model_lite_05_13_09_14/model_05_13_09_14.tflite'
model_path = './model_lite_05_13_09_14/model__subject-1_05_13_13_46.tflite'
interpreter = tf.lite.Interpreter(model_path=model_path)
interpreter.allocate_tensors()


classes_labels = ["break", "left_hand", "right_hand"]
actions = {'break':'rais_both_hands', 'left_hand':'rais_left_hand','right_hand':'rais_right_hand'}


def preprocess_data(arr):
    N_tr, N_ch, T = arr.shape 
    arr = arr.reshape(N_tr,1 , 1, N_ch, T)
    # arr = arr.reshape(1,1,14,1125)
    n_channels = 14
    for j in range(n_channels):
        scaler = StandardScaler()
        scaler.fit(arr[:,0,0,j,:])
        arr[:,0,0,j,:] = scaler.transform(arr[:,0,0,j,:])

    out_arr = arr.astype(np.float32)
    return out_arr
def inference(input_data):
    global interpreter
    
    

    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()
    y_pred = interpreter.get_tensor(output_details[0]['index'])
    return y_pred

def realtime_inference():
    import sub_stream_res

    n_predicts = 4
    input_arrs = np.zeros((0,14,1125))   
    output_arrs = np.zeros((0))
    for i in range(n_predicts):
        arr = sub_stream_res.main()[:1125,:]
        input_arrs = np.append(input_arrs,[arr.T],axis = 0)
    # print(input_arrs.shape)
    processed_input = preprocess_data(input_arrs)
    for i in range(n_predicts):
        output_i = np.argmax(inference(processed_input[i]))
        output_arrs = np.append(output_arrs,[output_i], axis=0)
    # print(output_arrs)
    output = np.argmax(np.bincount(output_arrs.astype('int64')))
    return output

def run_robot_action(predict):
    global classes_labels, actions
    label = classes_labels[predict]
    action = actions[label]
    if(action == 'rais_both_hands'):
        robot.BothHands_action.main()
    elif(action == 'rais_left_hand'):
        robot.LeftHand_action.main()
    elif(action == 'rais_right_hand'):
        robot.RightHand_action.main()
    else:
        print("error!")
    
if __name__  == "__main__":
    # test = preprocess_data(np.random.rand(4,14,1125))
    # print(test)
    # for i in range(3):
    while 1:
        input()
        pred = realtime_inference()
        run_robot_action(pred)
        print(classes_labels[pred])
        # input()