const express = require('express')
const bodyParser= require('body-parser')
const multer = require('multer');   
const cors = require('cors')
const fs = require('fs')
const spawn = require("child_process").spawn;

const port = process.env.PORT || 5000;
const app = express()

global.PROTO_PATH = __dirname+'/protos/prediction.proto'
const python_process = spawn("python",["deep-model/main.py"],{detached:true});

const makeDir = function(dir){
    if (!fs.existsSync(dir))
            fs.mkdirSync(dir, 0755);
}

const cleanExit = function() { process.exit() };
process.on('SIGINT', cleanExit); // catch ctrl-c
process.on('SIGTERM', cleanExit); // catch kill
process.on('exit', function() {
    python_process.kill()
});

app.use(cors())
app.use(bodyParser.urlencoded({extended: true}))
// app.use('/upload',express.static('uploads')) 

// app.all('/', function(req,res){
//     res.redirect('/api');
//     return
// });

app.use('/', express.static('./build', {
    index: "index.html"
}))
app.use('/api',require('./routes/api'));
app.use('*',(req,res)=>{
    return res.json("unknown url "+req.url)
});
 
app.listen(port, () =>{
    console.log(`Server started on port ${port}`)
    makeDir('./uploads')
    makeDir('./detection_output')
    makeDir('./output')
    
});


python_process.stdout.on('data', (data) => {
    console.log(`[python]: ${data}`);
 });
python_process.unref()