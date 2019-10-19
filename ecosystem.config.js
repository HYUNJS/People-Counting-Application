module.exports = {
  apps : [{
    name: 'lp-backend',
    script: 'index.js',

    // Options reference: https://pm2.io/doc/en/runtime/reference/ecosystem-file/
    autorestart: true,
    watch: false,
    error_file: "logs/error.log",
    out_file: "logs/out.log"
  }]
};
