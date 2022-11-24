import { Router, Request, Response } from "express";
import { validationResult, query } from "express-validator";
import { errorConst } from "../common/errorConstant";
import { HttpStatus } from "../common/httpStatus";
import { UserService } from "../service/user.service";

const router: Router = Router();
const testService = new UserService();

router.get(
  "/validate",
  [
    query(
      [
        "nationality",
        "passport_no",
        "national_identification",
        "name",
        "address",
      ],
      errorConst.errorInvalidInput
    ).optional(),
  ],
  async (req: Request, res: Response) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res
        .status(HttpStatus.STATUS_BAD_REQUEST)
        .send({ error: errors.array()[0]?.msg });
    } else {
      testService.testService(req, res);
    }
  }
);

export default router;
