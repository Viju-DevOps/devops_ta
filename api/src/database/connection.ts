import mysql from 'mysql';
import * as dotenv from "dotenv";

dotenv.config();
const createConnection = () => {
  return new Promise((resolve, reject) => {
    const pool = mysql.createConnection({
      user: process.env.DB_USERNAME,
      host: process.env.DB_HOST,
      database: process.env.DB_NAME,
      password: process.env.DB_PASSWORD,
      port: Number(process.env.DB_PORT),
    });

    pool.connect(function(err) {  
      if (err) 
        reject(err);  
      else
        resolve(pool); 
    }); 
  });
};

export default createConnection;
