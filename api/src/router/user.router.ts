import { Router, Request, Response } from "express";
import { validationResult, query, matchedData } from "express-validator";
import { errorConst } from "../common/errorConstant";
import { HttpStatus } from "../common/httpStatus";
import { UserService } from "../service/user.service";

const router: Router = Router();
const userService = new UserService();

router.get(
  "/validate",
  [
    query(
      [
        "name",
        "pob",
        "nationality",
        "passport_no",
        "address",
        // "national_identification_no",
        "drivers_license_no",
        "dob",
        "gender",
        "email"
      ],
      errorConst.errorInvalidInput
    ).optional(),
  ],
  async (req: Request, res: Response) => {
    const matchedParams = matchedData(req, {
      onlyValidData: true,
      includeOptionals: true,
      locations: ['query']
    })

    req.query = matchedParams;
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res
        .status(HttpStatus.STATUS_BAD_REQUEST)
        .send({ error: errors.array()[0]?.msg });
    } else {
      userService.validateUser(req, res);
    }
  }
);

export default router;
