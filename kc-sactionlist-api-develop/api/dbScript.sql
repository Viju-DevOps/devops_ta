CREATE OR REPLACE FUNCTION validate_user(
	user_email character varying default null,
	user_nationality character varying default null,
	user_passport_no character varying default null,
	user_national_identification_no character varying default null,
	user_drivers_license_no character varying default null,

	user_name character varying default null,
	user_dob character varying default null,
	user_pob character varying default null,
	user_address character varying default null,
	user_gender character varying default null,
	OUT primary_count integer,
	OUT secondary_count integer
)
AS $BODY$
DECLARE primaryTempListLength integer default 0;
DECLARE secondaryTempListLength integer default 0;
DECLARE primaryCheck integer default 0;
DECLARE nameCheck integer default 0;
DECLARE dobCheck integer default 0;
DECLARE pobCheck integer default 0;
DECLARE addressCheck integer default 0;
DECLARE genderCheck integer default 0;
DECLARE nationalityCheck integer default 0;
DECLARE nationalIdentificationNumberCheck integer default 0;
DECLARE drivingLicenseNumberCheck integer default 0;
DECLARE passportNumberCheck integer default 0;
BEGIN

-- primary check - email, nationality + passport no, nationality + driving license no, nationality + national ID
	SELECT 1 into primaryCheck
	FROM user_details
	WHERE 
	(
		(user_email IS NOT NULL AND (LOWER(BTRIM(user_email)) = ANY(LOWER((user_details.email_address)::text)::text[]))) OR 
		(user_passport_no IS NOT NULL AND user_nationality IS NOT NULL AND (
			(LOWER(ARRAY_TO_STRING((user_details.passport_no), '||')) LIKE '%' || LOWER(BTRIM(user_passport_no)) || '%') AND
			(LOWER(BTRIM(user_nationality)) = ANY(LOWER((user_details.nationality)::text)::text[]))
		 ))OR
		(user_drivers_license_no IS NOT NULL AND user_nationality IS NOT NULL AND (
			(BTRIM(LOWER(ARRAY_TO_STRING((user_details.drivers_license_no), '||'))) LIKE '%' || BTRIM(LOWER(user_drivers_license_no)) || '%')) AND
		 	(LOWER(BTRIM(user_nationality)) = ANY(LOWER((user_details.nationality)::text)::text[]))
		) OR 
		((LOWER(BTRIM(user_nationality)) = ANY(LOWER((user_details.nationality)::text)::text[])) AND
		 (user_national_identification_no IS NOT NULL AND (LOWER(BTRIM(user_national_identification_no)) = ANY(LOWER((user_details.national_identification_no)::text)::text[])))
		)
	)
		;

-- fuzzy logic - name, dob, pob, address, gender, nationality, National ID, Driving ID, passport no
	IF (primaryCheck != 1 OR primaryCheck IS NULL)
	THEN 	
	
-- 	name check
	CREATE TEMP TABLE primary_temp_list
	ON COMMIT DROP
	AS SELECT *
	FROM user_details
	WHERE (
		(user_name IS NOT NULL AND (LOWER(BTRIM(user_details.name)) = LOWER(BTRIM(user_name))) OR ((LOWER(user_name) = ANY(LOWER((user_details.alias_name_good_quality)::text)::text[]))) OR
        	(LOWER(user_name) = ANY(LOWER((user_details.alias_name_low_quality)::text)::text[]))) 
	);
	SELECT COUNT(*) INTO primaryTempListLength FROM primary_temp_list;
	SELECT COUNT(*) INTO secondaryTempListLength FROM user_details;
	
	IF(primaryTempListLength != 0 OR (primaryTempListLength = secondaryTempListLength))
	THEN
		nameCheck := 1;
	ELSE
		nameCheck := 0;
		INSERT INTO primary_temp_list
		SELECT * FROM user_details;
	END IF;
	
-- 	dob check
	CREATE TEMP TABLE secondary_temp_list
	ON COMMIT DROP
	AS SELECT *
	FROM primary_temp_list
	WHERE (
		(user_dob IS NOT NULL AND LOWER(BTRIM(user_dob)) = ANY(LOWER((primary_temp_list.dob)::text)::text[])) 
	);
	
	SELECT COUNT(*) INTO primaryTempListLength FROM primary_temp_list;
	SELECT COUNT(*) INTO secondaryTempListLength FROM secondary_temp_list;
	
	IF(secondaryTempListLength != 0 OR (primaryTempListLength = secondaryTempListLength))
	THEN
		dobCheck := 1;
	ELSE
		dobCheck := 0;
		TRUNCATE secondary_temp_list;
		INSERT INTO secondary_temp_list
		SELECT * FROM primary_temp_list;
	END IF;
	
-- 	pob check
	TRUNCATE TABLE primary_temp_list;

	INSERT INTO primary_temp_list 
	SELECT *
	FROM secondary_temp_list
	WHERE (
		(user_pob IS NOT NULL AND (LOWER(BTRIM(user_pob)) = ANY(LOWER((secondary_temp_list.pob)::text)::text[])))
	);
	
	SELECT COUNT(*) INTO primaryTempListLength FROM primary_temp_list;
	SELECT COUNT(*) INTO secondaryTempListLength FROM secondary_temp_list;

	IF(primaryTempListLength != 0 OR (primaryTempListLength = secondaryTempListLength))
	THEN
		pobCheck := 1;
	ELSE
		pobCheck := 0;
		TRUNCATE primary_temp_list;
		INSERT INTO primary_temp_list
		SELECT * FROM secondary_temp_list;
	END IF;
	
-- 	address check
	TRUNCATE TABLE secondary_temp_list;
	INSERT INTO secondary_temp_list 
	SELECT *
	FROM primary_temp_list
	WHERE (
		(user_address IS NOT NULL AND (BTRIM(LOWER(ARRAY_TO_STRING((primary_temp_list.address), '||'))) LIKE '%' || BTRIM(LOWER(BTRIM(user_address))) || '%'))
	);
	
	SELECT COUNT(*) INTO primaryTempListLength FROM primary_temp_list;
	SELECT COUNT(*) INTO secondaryTempListLength FROM secondary_temp_list;

	IF(secondaryTempListLength != 0 OR (primaryTempListLength = secondaryTempListLength))
	THEN
		addressCheck := 1;
	ELSE
		addressCheck := 0;
		TRUNCATE secondary_temp_list;
		INSERT INTO secondary_temp_list
		SELECT * FROM primary_temp_list;
	END IF;
	
-- 	check gender
	TRUNCATE TABLE primary_temp_list;
	INSERT INTO primary_temp_list 
	SELECT *
	FROM secondary_temp_list
	WHERE (
		(user_gender IS NOT NULL AND (LOWER(BTRIM(secondary_temp_list.gender)) = LOWER(BTRIM(user_gender))))
	);
	
	SELECT COUNT(*) INTO primaryTempListLength FROM primary_temp_list;
	SELECT COUNT(*) INTO secondaryTempListLength FROM secondary_temp_list;

	IF(primaryTempListLength != 0 OR (primaryTempListLength = secondaryTempListLength))
	THEN
		genderCheck := 1;
	ELSE
		genderCheck := 0;
-- 		TRUNCATE primary_temp_list;
		INSERT INTO primary_temp_list
		SELECT * FROM secondary_temp_list;
	END IF;

-- 	check Nationality
	TRUNCATE TABLE secondary_temp_list;
	INSERT INTO secondary_temp_list 
	SELECT *
	FROM primary_temp_list
	WHERE (
		(user_nationality IS NOT NULL AND (LOWER(BTRIM(user_nationality)) = ANY(LOWER((primary_temp_list.nationality)::text)::text[])))
	);
	
	SELECT COUNT(*) INTO primaryTempListLength FROM primary_temp_list;
	SELECT COUNT(*) INTO secondaryTempListLength FROM secondary_temp_list;

	IF(secondaryTempListLength != 0 OR (primaryTempListLength = secondaryTempListLength))
	THEN
		nationalityCheck := 1;
	ELSE
		nationalityCheck := 0;
		INSERT INTO secondary_temp_list
		SELECT * FROM primary_temp_list;
	END IF;
	
-- 	check National identification number
	TRUNCATE TABLE primary_temp_list;
	INSERT INTO primary_temp_list 
	SELECT *
	FROM secondary_temp_list
	WHERE (
		(user_national_identification_no IS NOT NULL AND (LOWER(BTRIM(user_national_identification_no)) = ANY(LOWER((secondary_temp_list.national_identification_no)::text)::text[])))
	);
	
	SELECT COUNT(*) INTO primaryTempListLength FROM primary_temp_list;
	SELECT COUNT(*) INTO secondaryTempListLength FROM secondary_temp_list;

	IF(primaryTempListLength != 0 OR (primaryTempListLength = secondaryTempListLength))
	THEN
		nationalIdentificationNumberCheck := 1;
	ELSE
		nationalIdentificationNumberCheck := 0;
		INSERT INTO primary_temp_list
		SELECT * FROM secondary_temp_list;
	END IF;

-- 	check Driving license number
	TRUNCATE TABLE secondary_temp_list;
	INSERT INTO secondary_temp_list 
	SELECT *
	FROM primary_temp_list
	WHERE (
		(user_drivers_license_no IS NOT NULL AND (BTRIM(LOWER(ARRAY_TO_STRING((primary_temp_list.drivers_license_no), '||'))) LIKE '%' || BTRIM(LOWER(user_drivers_license_no)) || '%'))
	);
	
	SELECT COUNT(*) INTO primaryTempListLength FROM primary_temp_list;
	SELECT COUNT(*) INTO secondaryTempListLength FROM secondary_temp_list;

	IF(secondaryTempListLength != 0 OR (primaryTempListLength = secondaryTempListLength))
	THEN
		drivingLicenseNumberCheck := 1;
	ELSE
		drivingLicenseNumberCheck := 0;
		INSERT INTO secondary_temp_list
		SELECT * FROM primary_temp_list;
	END IF;

-- 	check passport number
	TRUNCATE TABLE primary_temp_list;
	INSERT INTO primary_temp_list 
	SELECT *
	FROM secondary_temp_list
	WHERE (
		(user_passport_no IS NOT NULL AND (LOWER(ARRAY_TO_STRING((secondary_temp_list.passport_no), '||')) LIKE '%' || LOWER(BTRIM(user_passport_no)) || '%'))
	);
	
	SELECT COUNT(*) INTO primaryTempListLength FROM primary_temp_list;
	SELECT COUNT(*) INTO secondaryTempListLength FROM secondary_temp_list;

	IF(primaryTempListLength != 0 OR (primaryTempListLength = secondaryTempListLength))
	THEN
		passportNumberCheck := 1;
	ELSE
		passportNumberCheck := 0;
		INSERT INTO primary_temp_list
		SELECT * FROM secondary_temp_list;
	END IF;
	
END IF;

	SELECT COALESCE(primaryCheck,0) into primary_count;
	SELECT (
		COALESCE(nameCheck,0)+
		COALESCE(dobCheck,0)+
		COALESCE(pobCheck,0)+
		COALESCE(addressCheck,0)+
		COALESCE(genderCheck,0)+
        COALESCE(nationalityCheck,0)+
	    COALESCE(nationalIdentificationNumberCheck,0)+
        COALESCE(drivingLicenseNumberCheck)+
        COALESCE(passportNumberCheck)
	) INTO secondary_count;
	
END;
$BODY$
LANGUAGE plpgsql;