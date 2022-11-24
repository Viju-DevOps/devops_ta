import { Pool } from "pg";
import * as dotenv from "dotenv";

dotenv.config();
const createConnection = () => {
  return new Promise((resolve, reject) => {
    const pool = new Pool({
      user: process.env.DB_USERNAME,
      host: process.env.DB_HOST,
      database: process.env.DB_NAME,
      password: process.env.DB_PASSWORD,
      port: Number(process.env.DB_PORT),
    });

    pool
      .connect()
      .then(() => {
        resolve(pool);
      })
      .catch((error) => {
        reject(error);
      });
  });
};

export default createConnection;
