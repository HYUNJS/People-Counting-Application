<h1>Installation regarding web-server</h1>
<br>
<pre>
This system was tested to run under
    nodejs v10.16.0
    npm v6.10.0
    python v3.6.8
    
After satisfying upper requirements, please install required npm packages by <code>npm install</code>
Then, go to deep-model directory to install required python libraries.
Command is <code>pip3 install -U -r requirements.txt</code> . *use either pip or pip3 based on your system
</pre>

<h1>How to run the program</h1>
<pre>
Run command: <code>node index.js</code>  under the root directory of project
Or, you can use process manager program such as pm2.
In this project I used pm2 and you can start by <code>pm2 start ecosystem.config.js</code>
</pre>
