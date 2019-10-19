Installation regarding web-server

This system is able to run on
    nodejs v10.16.0
    npm v6.10.0
    python v3.6.8

After satisfying upper requirements, please install required packages by 'npm install'


Installation regarding yolo-model
1. go to directory yolo-module. Following instructions suppose under yolo-module directory
2. mkdir weights
3. download pretrained weights from these links and place them under directory 'weights'
detection model: https://hkustconnect-my.sharepoint.com/:u:/g/personal/jhyunaa_connect_ust_hk/Eb73mEEZ5-9Dl2m-kfLl9JEB28GOkwXAq5LCBylJ406P5g?e=CjrM4H
recognition model: https://hkustconnect-my.sharepoint.com/:u:/g/personal/jhyunaa_connect_ust_hk/EWEqXx3qTZlIlp8JNQuiERQBb5cy3lQN2ca_EfHJtEq_aw?e=mtFhBX

You can download in terminal by:
wget https://hkustconnect-my.sharepoint.com/:u:/g/personal/jhyunaa_connect_ust_hk/Eb73mEEZ5-9Dl2m-kfLl9JEB28GOkwXAq5LCBylJ406P5g?download=1
wget https://hkustconnect-my.sharepoint.com/:u:/g/personal/jhyunaa_connect_ust_hk/EWEqXx3qTZlIlp8JNQuiERQBb5cy3lQN2ca_EfHJtEq_aw?download=1

Then rename it by:
mv Eb73mEEZ5-9Dl2m-kfLl9JEB28GOkwXAq5LCBylJ406P5g\?download\=1 best_detection.weights
mv EWEqXx3qTZlIlp8JNQuiERQBb5cy3lQN2ca_EfHJtEq_aw\?download\=1 best_recognition.pt

4. create virtualenv for yolo module packages 'virutalenv env'
5. download required packages for yolo moudle in virtualenv
env/bin/pip install -r requirements.txt


How to run the program
Simply
    node index.js under the root directory of project
Or, you can use process manager program such as pm2
In this case, pm2 start ecosystem.config.js
