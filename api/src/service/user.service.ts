import { Request, Response } from "express";
import { HttpStatus } from "../common/httpStatus";
import { responseMessage } from "../common/responseMessage";
import server from "../app";
import { errorHandler } from "../middleware/errorHandler.middleware";
import { ValidateUserQueryInfo } from "model/interface/query_info";

export class UserService {
  public validateUser = async (req: Request, res: Response) => {
    try {
      const queryData: ValidateUserQueryInfo = req.query;
      const validParams = Object.values(queryData).filter(
        (value: string) =>
          value?.length !== 0 && value !== null && value !== undefined
      );
      const totalParamCount = validParams.length;
      let genderData = queryData?.gender;

      if(queryData?.gender?.toLowerCase() === "m"){
        genderData = "male";
      }
      else if(queryData?.gender?.toLowerCase() === "f"){
        genderData = "female";
      }
      else{
        genderData = queryData?.gender;
      }

      await server.dbConnection.query(
        `CALL validate_user(
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
        ${queryData?.dob ? "'" + String(queryData?.dob) + "'" : null},
        ${queryData?.pob ? "'" + String(queryData?.pob) + "'" : null},
        ${queryData?.address ? "'" + String(queryData?.address) + "'" : null},
        ${genderData ? "'" + String(genderData) + "'" : null}
        )`,
        (err: any, row: any) => {
          if (err) {
            return errorHandler(err, req, res);
          } else {
            return res.status(HttpStatus.STATUS_OK).send({
              message: responseMessage?.VALIDATIONDATAFETCHSUCCESS,
              validationResult: Number(row[0][0]?.primary_count === 1)
                ? row[0][0]?.primary_count
                : Number(row[0][0]?.secondary_count) / Number(totalParamCount),
            });
          }
        }
      );
    } catch (error: any) {
      return errorHandler(error, req, res);
    }
  };
}
