DELIMITER $$
DROP PROCEDURE IF EXISTS `validate_user`$$
CREATE PROCEDURE `validate_user`(
	IN `user_email` TEXT,
    IN `user_nationality` TEXT,
    IN `user_passport_no` TEXT,
    IN `user_national_identification_no` TEXT,
    IN `user_drivers_license_no` TEXT,
    
    IN `user_name` TEXT,
    IN `user_dob` TEXT,
    IN `user_pob` TEXT,
    IN `user_address` TEXT,
    IN `user_gender` TEXT
    )
BEGIN
	DECLARE primaryTempListLength INT DEFAULT 0;
    DECLARE secondaryTempListLength INT DEFAULT 0;
    DECLARE primaryCheck INT DEFAULT 0;
    DECLARE nameCheck INT DEFAULT 0;
    DECLARE dobCheck FLOAT(6,3) DEFAULT 0.000;
    DECLARE pobCheck FLOAT(6,3) DEFAULT 0;
    DECLARE addressCheck FLOAT(6,3) DEFAULT 0;
    DECLARE genderCheck INT DEFAULT 0;
    DECLARE nationalityCheck INT DEFAULT 0;
    DECLARE nationalIdentificationNumberCheck INT DEFAULT 0;
    DECLARE drivingLicenseNumberCheck INT DEFAULT 0;
    DECLARE passportNumberCheck INT DEFAULT 0;
    DECLARE userDobLength INT DEFAULT 0;
    
--   primary check - email, nationality + passport no, nationality + driving license no, nationality + national ID
	SELECT 1 into primaryCheck
	FROM sanctions_list
	WHERE 
	(
		(user_email IS NOT NULL AND (LOWER(TRIM(user_email)) = LOWER(TRIM(sanctions_list.email_address)))) OR
        (user_passport_no IS NOT NULL AND user_nationality IS NOT NULL AND (
            (JSON_SEARCH(LOWER(TRIM(sanctions_list.passport_no)), 'one', (CONCAT('%', (LOWER(TRIM(user_passport_no))))), '%')) AND
			((LOWER(TRIM(user_nationality))) MEMBER OF (LOWER(TRIM(sanctions_list.nationality))))
		)) OR
		(user_drivers_license_no IS NOT NULL AND user_nationality IS NOT NULL AND (
			((LOWER(TRIM(user_nationality))) MEMBER OF (LOWER(TRIM(sanctions_list.nationality)))) AND
			(JSON_SEARCH(LOWER(TRIM(sanctions_list.drivers_license_no)), 'one', (CONCAT('%', (LOWER(TRIM(user_drivers_license_no))))), '%'))
		))
	);
    
-- fuzzy logic - name, dob, pob, address, gender, nationality, National ID, Driving ID, passport no
	IF (primaryCheck != 1 OR primaryCheck IS NULL)
		THEN
	-- name check
		DROP TEMPORARY TABLE IF EXISTS primary_temp_list;
		CREATE TEMPORARY TABLE IF NOT EXISTS primary_temp_list
		AS SELECT *
		FROM sanctions_list
		WHERE (
			(user_name IS NOT NULL AND (LOWER(TRIM(sanctions_list.name)) = LOWER(TRIM(user_name))) OR 
			(LOWER(TRIM(user_name)) MEMBER OF (LOWER(TRIM(sanctions_list.alias_name_good_quality)))) OR
			(LOWER(TRIM(user_name)) MEMBER OF (LOWER(TRIM(sanctions_list.alias_name_low_quality)))))
		);
		SELECT COUNT(*) INTO primaryTempListLength FROM primary_temp_list;
		SELECT COUNT(*) INTO secondaryTempListLength FROM sanctions_list;
		
		IF(primaryTempListLength != 0 OR (primaryTempListLength = secondaryTempListLength))
		THEN
			SET nameCheck = 1;
		ELSE
			SET nameCheck = 0;
			INSERT INTO primary_temp_list
			SELECT * FROM sanctions_list;
		END IF;
	
    -- 	check gender
        DROP TEMPORARY TABLE IF EXISTS secondary_temp_list;
        CREATE TEMPORARY TABLE IF NOT EXISTS secondary_temp_list 
        SELECT *
        FROM primary_temp_list
        WHERE (
            (user_gender IS NOT NULL AND (LOWER(TRIM(primary_temp_list.gender)) = LOWER(TRIM(user_gender))))
        );
        
        SELECT COUNT(*) INTO primaryTempListLength FROM primary_temp_list;
        SELECT COUNT(*) INTO secondaryTempListLength FROM secondary_temp_list;

        IF(secondaryTempListLength != 0 OR (primaryTempListLength = secondaryTempListLength))
        THEN
            SET genderCheck = 1;
        ELSE
            SET genderCheck = 0;
            TRUNCATE secondary_temp_list;
            INSERT INTO secondary_temp_list
            SELECT * FROM primary_temp_list;
        END IF;
        
	-- 	dob check
		IF(YEAR(user_dob)>0)
        THEN
            SET userDobLength = (userDobLength + 1);
        END IF;

        IF(MONTH(user_dob)>0)
        THEN
            SET userDobLength = (userDobLength + 1);
        END IF;

        IF(DAY(user_dob)>0)
        THEN
            SET userDobLength = (userDobLength + 1);
        END IF;

        IF(SELECT COUNT(*) FROM secondary_temp_list WHERE user_dob MEMBER OF (secondary_temp_list.dob))
		THEN
			SET dobCheck = 1;
		ELSE
			IF(SELECT COUNT(*) FROM secondary_temp_list WHERE (
				JSON_SEARCH(secondary_temp_list.dob, 'one', (CONCAT(DATE_FORMAT(user_dob,'%Y'),'-',DATE_FORMAT(user_dob,'%m'),'-%'))) OR
                JSON_SEARCH(secondary_temp_list.dob, 'one', (CONCAT(DATE_FORMAT(user_dob,'%Y'),'-%-',DATE_FORMAT(user_dob,'%d')))) OR
				JSON_SEARCH(secondary_temp_list.dob, 'one', (CONCAT('%-',DATE_FORMAT(user_dob,'%m'),'-',DATE_FORMAT(user_dob,'%d'))))
                ))
            THEN
				SET dobCheck = (2/userDobLength);
			ELSEIF(SELECT COUNT(*) FROM secondary_temp_list WHERE (
				JSON_SEARCH(secondary_temp_list.dob, 'one', (CONCAT(DATE_FORMAT(user_dob,'%Y'),'-%'))) OR
                JSON_SEARCH(secondary_temp_list.dob, 'one', (CONCAT('%-', DATE_FORMAT(user_dob,'%m'), '-%'))) OR
                JSON_SEARCH(secondary_temp_list.dob, 'one', (CONCAT('%-', DATE_FORMAT(user_dob,'%d')))) OR
                JSON_SEARCH(secondary_temp_list.dob, 'one', (DATE_FORMAT(user_dob,'%Y')))
                ))
			THEN
				SET dobCheck = (1/userDobLength);
			END IF;
		END IF;

	-- 	pob check
		SET pobCheck = (SELECT validate_pob(user_pob, 'secondary_temp_list'));
        
	-- address check
		SET addressCheck = (SELECT validate_address(user_address, 'secondary_temp_list'));
        
	-- check Nationality
        SELECT 1 INTO nationalityCheck
        FROM secondary_temp_list
        WHERE (
            (user_nationality IS NOT NULL AND (LOWER(TRIM(user_nationality)) MEMBER OF (LOWER(secondary_temp_list.nationality))))
        );
        
	-- 	check passport number
		SELECT 1 INTO passportNumberCheck
        FROM secondary_temp_list
        WHERE (
            (user_passport_no IS NOT NULL AND (
				JSON_SEARCH(LOWER(TRIM(secondary_temp_list.passport_no)), 'one', (CONCAT('%', (LOWER(TRIM(user_passport_no))))), '%')
			))
        );
    
	-- 	check Driving license number
		SELECT 1 INTO drivingLicenseNumberCheck
		FROM secondary_temp_list
		WHERE (
			(user_drivers_license_no IS NOT NULL AND (
				JSON_SEARCH(LOWER(TRIM(secondary_temp_list.drivers_license_no)), 'one', (CONCAT('%', (LOWER(TRIM(user_drivers_license_no))))), '%')
			))
		);
	END IF;
    
    SELECT COALESCE(primaryCheck,0) AS primary_count, (
		COALESCE(nameCheck,0)+
		COALESCE(dobCheck,0)+
		COALESCE(pobCheck,0)+
		COALESCE(addressCheck,0)+
		COALESCE(genderCheck,0)+
        COALESCE(nationalityCheck,0)+
	    COALESCE(nationalIdentificationNumberCheck,0)+
        COALESCE(drivingLicenseNumberCheck)+
        COALESCE(passportNumberCheck)
	) AS secondary_count;
    
END$$
DELIMITER ;



-- function to validate POB
DELIMITER //

DROP FUNCTION IF EXISTS validate_pob;
CREATE FUNCTION validate_pob(user_pob TEXT, data_table TEXT) 
RETURNS FLOAT(6,3) DETERMINISTIC
BEGIN
DECLARE pobCheck1 FLOAT(6,3) DEFAULT 0.000;
DECLARE pobCheck2 FLOAT(6,3) DEFAULT 0.000;
DECLARE inputStringLength INT DEFAULT 0;
DECLARE length INT DEFAULT 0;
DECLARE counter INT DEFAULT 0;
DECLARE stringCounter INT DEFAULT 0;
DECLARE subString TEXT DEFAULT '';
DECLARE isDataFound INT DEFAULT 0;
 
 SET inputStringLength = (SELECT SUM(LENGTH(user_pob) - LENGTH(REPLACE(	user_pob, ',', '')) + 1));
 SELECT COUNT(*) FROM secondary_temp_list INTO length;
 SET counter=0;
 tableLoop: WHILE (counter<length) DO
  SET stringCounter = 1;
  SET pobCheck1 = 0;

  inputStringLoop: WHILE stringCounter<=inputStringLength DO
	SET subString = null;
	SET subString = (SELECT SUBSTRING_INDEX(SUBSTRING_INDEX(user_pob,',', stringCounter), ',',-1)); -- get substring
	
    SET isDataFound = 0;
    SELECT 1 INTO isDataFound FROM secondary_temp_list WHERE subString IS NOT NULL AND (LOWER(TRIM(subString))) MEMBER OF (LOWER(TRIM(secondary_temp_list.pob))) LIMIT counter,1;

    IF(isDataFound = 1)
	THEN
		SET pobCheck1 = (pobCheck1+(1/inputStringLength));
	END IF;

    SET stringCounter = stringCounter + 1;
  END WHILE inputStringLoop;
  
  IF(pobCheck1 = 1)
  THEN
	SET pobCheck2 = pobCheck1;
    LEAVE tableLoop;
  ELSEIF((pobCheck1 != 0.000) AND (pobCheck2 < pobCheck1)) THEN
	SET pobCheck2 = pobCheck1;
    SET counter = counter + 1;
  ELSE 
	SET counter = counter + 1;
  END IF;
END WHILE tableLoop;
RETURN pobCheck2;

END 

//
DELIMITER ;


-- function to validate address
DELIMITER //
DROP FUNCTION IF EXISTS validate_address;
CREATE FUNCTION validate_address (user_address TEXT, data_table TEXT)
RETURNS FLOAT(6,3) DETERMINISTIC

BEGIN
DECLARE addressCheck1 FLOAT(6,3) DEFAULT 0.000;
DECLARE addressCheck2 FLOAT(6,3) DEFAULT 0.000;
DECLARE inputStringLength INT DEFAULT 0;
DECLARE length INT DEFAULT 0;
DECLARE counter INT DEFAULT 0;
DECLARE stringCounter INT DEFAULT 0;
DECLARE subString TEXT DEFAULT '';
DECLARE isDataFound INT DEFAULT 0;

SET inputStringLength = (SELECT SUM(LENGTH(user_address) - LENGTH(REPLACE(	user_address, ',', '')) + 1));
 SELECT COUNT(*) FROM secondary_temp_list INTO length;
 SET counter=0;
  tableLoop: WHILE (counter<length) DO
  SET stringCounter = 1;
  SET addressCheck1 = 0;

  inputStringLoop: WHILE stringCounter<=inputStringLength DO
	SET subString = null;
	SET subString = (SELECT SUBSTRING_INDEX(SUBSTRING_INDEX(user_address,',', stringCounter), ',',-1)); -- get substring
	
    SET isDataFound = 0;
    SELECT 1 INTO isDataFound FROM secondary_temp_list WHERE subString IS NOT NULL AND (LOWER(TRIM(subString))) MEMBER OF (LOWER(TRIM(address))) LIMIT counter,1;

    IF(isDataFound = 1)
	THEN
		SET addressCheck1 = (addressCheck1+(1/inputStringLength));
	END IF;

    SET stringCounter = stringCounter + 1;
  END WHILE inputStringLoop;
  
  IF(addressCheck1 = 1)
  THEN
	SET addressCheck2 = addressCheck1;
    LEAVE tableLoop;
  ELSEIF((addressCheck1 != 0.000) AND (addressCheck2 < addressCheck1)) THEN
	SET addressCheck2 = addressCheck1;
    SET counter = counter + 1;
  ELSE 
	SET counter = counter + 1;
  END IF;
END WHILE tableLoop;

   RETURN addressCheck2;

END; //

DELIMITER ;