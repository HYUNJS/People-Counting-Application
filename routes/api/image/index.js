const router = require('express').Router()
const path = require('path')
const fs = require('fs')
const multer = require('multer')
const image2base64 = require('image-to-base64');

const grpc = require('grpc');
const protoLoader = require('@grpc/proto-loader');
const packageDefinition = protoLoader.loadSync(
    global.PROTO_PATH,
    {keepCase: true,
     longs: String,
     enums: String,
     defaults: true,
     oneofs: true
    });
// const prediction_proto = grpc.loadPackageDefinition(packageDefinition).prediction;
const prediction_proto = grpc.loadPackageDefinition(packageDefinition);
// console.log("[prediction_proto]\n",prediction_proto)

var timestamp = ''
var ip =  '' 
let client_id = ''

const deleteFolderRecursive = function(path) {
    if (fs.existsSync(path)) {
        fs.readdirSync(path).forEach(function(file, index){
            let curPath = path + "/" + file;
            if (fs.lstatSync(curPath).isDirectory()) { // recurse
                deleteFolderRecursive(curPath);
            } else { // delete file
                fs.unlinkSync(curPath);
            }
        });
        fs.rmdirSync(path);
    }
};

const upload = multer({
  storage: multer.diskStorage({
    destination: function (req, file, cb) {
        timestamp = Date.now()
        ip = req.header('x-forwarded-for') || req.connection.remoteAddress
        ip = ip.replace(new RegExp(':', 'g'), '-');
        client_id = timestamp+"_"+ip
        let dir = './uploads/'+client_id;
        if (!fs.existsSync(dir))
            fs.mkdirSync(dir, 0755);
        
        cb(null, 'uploads/'+client_id+"/");
    },
    filename: function (req, file, cb) {
        // cb(null, Date.now() + '-' + file.originalname);
        cb(null, file.originalname);
    }
  }),
});

router.get('/upload',(req,res)=>{
  console.log("upload GET")
  res.status(200).json({
    "message": "Hello from upload"
  })
})

router.post('/upload', upload.single('img'), (req, res) => {
//router.post('/upload', (req, res) => {
    console.log(new Date()+": upload post request incoming")
    
    console.log('BODY')
    console.log(req.body)

    console.log('Parameter')
    console.log(req.params)
    


    const client = new prediction_proto.Predictor('localhost:50051', grpc.credentials.createInsecure());
    client.prediction({image_dir: client_id}, function(err,response) {
        console.log('Response:', response);
        console.log("ERR: ",err)
        
        let result = response.message

        req.file.originalname = client_id+ "/" + req.file.originalname

        if(fs.existsSync('output/'+req.file.originalname)){
            image2base64('output/'+req.file.originalname) // you can also to use url
            .then((img) => {
                res.status(200).json({
                    'result':result,
                    'imageUrl':'data:image/jpeg;base64,'+img
                })
            }).catch((error) => {
                console.log(error);
                res.status(500).json({
                    'msg': error
                })
            })
        }else{
        console.log("There is no detected people")
            res.status(500).json({
                'msg': "Fail to Detect"
            })
        }

        console.log("Response is sent! Now remove the uploaded file and output folder")

        // fs.unlinkSync('./uploads/'+req.file.originalname)
        // deleteFolderRecursive('./output/')
        
        // deleteFolderRecursive('./uploads/'+client_id+"/")
        // deleteFolderRecursive('./detection_output/'+client_id+"/")
        // deleteFolderRecursive('./output/'+client_id+"/")
    });
});

  module.exports = router
