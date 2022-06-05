SELECT
	DISTINCT CASE
		WHEN tst.visit_date BETWEEN '2016-10-01'
		AND '2017-09-30' THEN 'Steps_FY1'
		WHEN tst.visit_date BETWEEN '2017-10-01'
		AND '2018-09-30' THEN 'Steps_FY2'
		WHEN tst.visit_date BETWEEN '2018-10-01'
		AND '2019-09-30' THEN 'Steps_FY3'
		WHEN tst.visit_date BETWEEN '2019-10-01'
		AND '2020-09-30' THEN 'Steps_FY4'
		WHEN tst.visit_date BETWEEN '2020-10-01'
		AND '2021-09-30' THEN 'Steps_FY5'
		WHEN tst.visit_date BETWEEN '2021-10-01'
		AND '2022-09-30' THEN 'Vukisha_FY1'
		WHEN tst.visit_date BETWEEN '2022-10-01'
		AND '2023-09-30' THEN 'Vukisha_FY2'
		WHEN tst.visit_date BETWEEN '2023-10-01'
		AND '2024-09-30' THEN 'Vukisha_FY3'
		WHEN tst.visit_date BETWEEN '2024-10-01'
		AND '2025-09-30' THEN 'Vukisha_FY4'
		WHEN tst.visit_date BETWEEN '2025-10-01'
		AND '2026-09-30' THEN 'Vukisha_FY5'
	END AS 'Financial_Year',
	YEAR(tst.visit_date) AS 'Year',
	MONTHNAME(tst.visit_date) AS 'Month',
	DAY(tst.visit_date) AS 'Date',
	UPPER(pd.given_name) AS 'First Name',
	UPPER(pd.middle_name) AS 'Middle Name',
	UPPER(pd.family_name) AS 'Last Name',
	pd.Gender AS 'Gender',
	YEAR(CURDATE()) - YEAR(pd.dob) AS 'Age',
	CASE
		WHEN co.unique_identifier LIKE '%45266%' THEN 'Nyaribari Masaba'
		WHEN co.unique_identifier LIKE '%45262%' THEN 'South Mugirango'
		WHEN co.unique_identifier LIKE '%45264%' THEN 'Bobasi'
		WHEN co.unique_identifier LIKE '%45261%' THEN 'Bonchari'
		WHEN co.unique_identifier LIKE '%45269%' THEN 'Kitutu Chache South'
		ELSE 'Unknown'
	END AS 'Sub_County',
	tst.setting as 'Setting',
	CASE
		WHEN CASE
			WHEN co.key_population_type IS NULL THEN 'General Population'
			ELSE co.key_population_type
		END = 'General Population' THEN 'General Population'
		ELSE 'KeyPopulation'
	END AS 'PopulationType',
	CASE
		WHEN tst.test_strategy != '' THEN 'VCT'
		ELSE 'PNS'
	END AS 'Strategy',
	CASE
		WHEN co.key_population_type IS NULL THEN 'General Population'
		ELSE co.key_population_type
	END AS 'KeyPopulationType',
	tst.final_test_result AS 'HTSResult',
	CASE
		WHEN tst.final_test_result = 'Negative' THEN 'N/A'
		WHEN tst.final_test_result = 'Positive'
		AND l.visit_date IS NOT NULL THEN 'Linked'
		WHEN tst.final_test_result = 'Positive'
		AND l.visit_date IS NULL THEN 'Not Linked'
	END AS 'LinkageStatus',
	UPPER(p.provider) AS 'Provider'
FROM
	kenyaemr_etl.etl_hts_test tst
	LEFT JOIN kenyaemr_etl.etl_patient_demographics pd ON pd.patient_id = tst.patient_id
	LEFT JOIN kenyaemr_etl.etl_clinical_visit cv ON tst.patient_id = cv.client_id
	LEFT JOIN kenyaemr_etl.etl_contact co ON co.client_id = tst.patient_id
	LEFT JOIN kenyaemr_etl.etl_hts_referral_and_linkage l ON l.patient_id = tst.patient_id
	LEFT JOIN kenyaemr_etl.etl_provider p ON p.creator_id = tst.creator
ORDER BY
	tst.date_created,CASE
		WHEN co.key_population_type IS NULL THEN 'General Population'
		ELSE co.key_population_type
	END