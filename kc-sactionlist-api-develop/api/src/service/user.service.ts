import { Request, Response } from "express";
import moment from "moment";
import { HttpStatus } from "../common/httpStatus";
import { responseMessage } from "../common/responseMessage";
import server from "../app";
import { errorHandler } from "../middleware/errorHandler.middleware";

export class UserService {
  public testService = async (req: Request, res: Response) => {
    try {
      const queryData: any = req.query;
      let totalParamCount = 0;
      if (queryData?.name) {
        totalParamCount = totalParamCount + 1;
      }
      if (queryData?.original_script) {
        totalParamCount = totalParamCount + 1;
      }
      if (queryData?.title) {
        totalParamCount = totalParamCount + 1;
      }
      if (queryData?.designation) {
        totalParamCount = totalParamCount + 1;
      }
      if (queryData?.pob) {
        totalParamCount = totalParamCount + 1;
      }
      if (queryData?.nationality) {
        totalParamCount = totalParamCount + 1;
      }
      if (queryData?.passport_no) {
        totalParamCount = totalParamCount + 1;
      }
      if (queryData?.address) {
        totalParamCount = totalParamCount + 1;
      }
      if (queryData?.national_identification_no) {
        totalParamCount = totalParamCount + 1;
      }
      if (queryData?.national_identification_detail) {
        totalParamCount = totalParamCount + 1;
      }
      if (queryData?.drivers_license_no) {
        totalParamCount = totalParamCount + 1;
      }
      if (queryData?.dob) {
        totalParamCount = totalParamCount + 1;
      }
      if (queryData?.gender) {
        totalParamCount = totalParamCount + 1;
      }
      if (queryData?.identification_no) {
        totalParamCount = totalParamCount + 1;
      }
      if (queryData?.email) {
        totalParamCount = totalParamCount + 1;
      }
      if (queryData?.position) {
        totalParamCount = totalParamCount + 1;
      }

      let genderData = queryData?.gender;
      switch (queryData?.gender) {
        case queryData?.gender?.toLowerCase() === "m":
          genderData = "male";
          break;
        case queryData?.gender?.toLowerCase() === "f":
          genderData = "female";
          break;
        default:
          genderData = queryData?.gender;
          break;
      }

      let dobData = queryData?.dob;
      const formattedDate = new Date("queryData?.dob");
      if (
        queryData?.dob &&
        formattedDate?.getDate() !== 0 &&
        formattedDate?.getTime() > 0
      ) {
        dobData = moment(queryData?.dob)?.format("DD/MM/YYYY");
      } else {
        dobData = queryData?.dob;
      }

      const userData = await server.dbConnection
        .query(`SELECT * FROM validate_user(
        ${queryData?.email ? "'" + String(queryData?.email) + "'" : null},
        ${
          queryData?.nationality
            ? "'" + String(queryData?.nationality) + "'"
            : null
        },
        ${
          queryData?.passport_no
            ? "'" + String(queryData?.passport_no) + "'"
            : null
        },
        ${
          queryData?.national_identification_no
            ? "'" + String(queryData?.national_identification_no) + "'"
            : null
        },
        ${
          queryData?.drivers_license_no
            ? "'" + String(queryData?.drivers_license_no) + "'"
            : null
        },
        ${queryData?.name ? "'" + String(queryData?.name) + "'" : null},
        ${dobData ? "'" + String(dobData) + "'" : null},
        ${queryData?.pob ? "'" + String(queryData?.pob) + "'" : null},
        ${queryData?.address ? "'" + String(queryData?.address) + "'" : null},
        ${genderData ? "'" + String(genderData) + "'" : null}
        )`);

      return res.status(HttpStatus.STATUS_OK).send({
        messge: responseMessage?.VALIDATIONDATAFETCHSUCCESS,
        validationResult: Number(userData?.rows[0]?.primary_count === 1)
          ? userData?.rows[0]?.primary_count
          : Number(userData?.rows[0]?.secondary_count) /
            Number(totalParamCount),
      });
    } catch (error: any) {
      console.log("error:::", error);
      return errorHandler(error, req, res);
    }
  };
}
