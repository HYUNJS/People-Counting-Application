const router = require('express').Router();
const cors = require('cors')

router.options('/image',cors())

router.get('/',(req,res)=>{
  return res.status(200).json({message: 'Prototype for people counting application'})
})

router.use('/image', require('./image'));

router.all('*', (req, res) => {
  res.status(404).send({ success: false, msg: `unknown uri ${req.path}` });
});

module.exports = router;
