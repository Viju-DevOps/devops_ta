import express from "express";
import UserRouter from "../router/user.router";

const RouterManager = express.Router();

RouterManager.use("/user", UserRouter);

export default RouterManager;
