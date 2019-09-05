*************************************************************************
*                                                                       *
*                       24662 RS IoT course project                     *
*                                                                       *
*                              GESTURE SOCCER                           *
*************************************************************************

TEAM: ===================================================================
Han-Yu Lee
Michael Graesser
Tzu-Chieh Tai
Yuhe Fu
Yixiao Fang

DESCRIPTION: ============================================================
Gesture soccer is a game that 2 people compete with each other by gesture-commanding pycars to score goals.
Machine learning (namely neural networks) is used to learn various gestures. 
There are a total of 11 gestures.
Hand positions are gathered with LEAP motion sensors real-time.
Then these hand positions are decoded into car-commanding codes and uploaded to the Cerlab server.
Then pycar download these commands and performs the specified commands.

CODES: ==================================================================
    *** Machine learning ***
        "static_data_collection_v1.py" is used to collect and save data recorded from LEAP motion.
            Change 'person' and 'tag' in the file to save different gestures.
        "train_net.py" is used to read in the recorded data and train the neural network and then save the trained model as a session.
        "leap_node_ver5.py" is responsible for real-time processing the position data gathered from LEAP motion and send them to the local server for decoding. 
        "tensorflow_localServer_ver4.py" is responsible for decoding the real-time data sent from leap_node_ver5.py and upload the decoded command to the server.

        All the other files are supporting files needed to run the code.

        Trained models:
            are saved in the "model" folder.
            For general purpose, please use model 563.
            Other models are the testing model the team is using.
        Loading models:
            In "tensorflow_localServer_ver4.py",
            There are 2 lines:
            "saver = tf.train.import_meta_graph("./model/MODEL_NAME/model.ckpt.meta")"
            "saver.restore(sess, "./model/MODEL_NAME/model.ckpt")"
            change MODEL_NAME to the model name you are using.
            For example, for model 563, these 2 lines should read:
            "saver = tf.train.import_meta_graph("./model/563/model.ckpt.meta")"
            "saver.restore(sess, "./model/563/model.ckpt")"
            Make sure the model you are using is in the "model" folder.
        Running gesture soccer:
            Have python3 environment run "tensorflow_localServer_ver4.py" first. Then have python2 environment run "leap_node_ver5.py".
            Have LEAP motion connected to the computer running these codes.
            Gesture above LEAP motion, and the code will do the rest.

    *** pointing ***
    *** PHP server ***
    *** Pycar control ***



