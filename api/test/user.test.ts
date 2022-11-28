import request from "supertest";
import { expect, test, describe } from "@jest/globals";
import server from "../src/app";

describe("User Details", () => {
  const datas = [
    {
      nationality: "test",
      // passport_no: "",
      // national_identification: "",
      // name: "",
      // address: "",
    },

    {
      // nationality: "no",
      passport_no: "test",
      // national_identification: "",
      // name: "",
      // address: "",
    },
    // {
    //   // nationality: "no",
    //   // passport_no: "",
    //   national_identification: "test",
    //   // name: "",
    //   // address: "",
    // },
    {
      // nationality: "no",
      // passport_no: "",
      // national_identification: "",
      name: "test",
      // address: "",
    },
    {
      // nationality: "no",
      // passport_no: "",
      // national_identification: "",
      // name: "",
      address: "test",
    },
  ];
  test.each(datas)("Check User Details response", async (...params) => {
    const app = await server.getApp();
    const res: any = await request(app)
      .get("/api/user/validate")
      .query({ ...params })
      .expect(200);
    expect(res?.body?.validationResult).toBeDefined();
  });
});
