SELECT
	DISTINCT CASE
		WHEN hv.visit_date BETWEEN '2016-10-01'
		AND '2017-09-30' THEN 'Steps_FY1'
		WHEN hv.visit_date BETWEEN '2017-10-01'
		AND '2018-09-30' THEN 'Steps_FY2'
		WHEN hv.visit_date BETWEEN '2018-10-01'
		AND '2019-09-30' THEN 'Steps_FY3'
		WHEN hv.visit_date BETWEEN '2019-10-01'
		AND '2020-09-30' THEN 'Steps_FY4'
		WHEN hv.visit_date BETWEEN '2020-10-01'
		AND '2021-09-30' THEN 'Steps_FY5'
		WHEN hv.visit_date BETWEEN '2021-10-01'
		AND '2022-09-30' THEN 'Vukisha_FY1'
		WHEN hv.visit_date BETWEEN '2022-10-01'
		AND '2023-09-30' THEN 'Vukisha_FY2'
		WHEN hv.visit_date BETWEEN '2023-10-01'
		AND '2024-09-30' THEN 'Vukisha_FY3'
		WHEN hv.visit_date BETWEEN '2024-10-01'
		AND '2025-09-30' THEN 'Vukisha_FY4'
		WHEN hv.visit_date BETWEEN '2025-10-01'
		AND '2026-09-30' THEN 'Vukisha_FY5'
	END AS 'Financial_Year_',
	MONTHNAME(hv.visit_date) AS 'Month',
	DAY(hv.visit_date) AS 'Date',
	pd.given_name AS 'First Name',
	pd.middle_name AS 'Middle Name',
	pd.family_name AS 'Last Name',
	pd.Gender AS 'Gender',
	YEAR(CURDATE()) - YEAR(pd.dob) AS 'Age',
	CASE
		WHEN CASE
			WHEN co.key_population_type IS NULL THEN 'General Population'
			ELSE co.key_population_type
		END = 'General Population' THEN 'General Population'
		ELSE 'KeyPopulation'
	END AS 'PopulationType',
	CASE
		WHEN co.key_population_type IS NULL THEN 'General Population'
		ELSE co.key_population_type
	END AS 'KeyPopulationType',
	CASE
		WHEN tx.visit_date IS NULL THEN 'Incative'
		ELSE 'On ART'
	END AS 'Status',
	CASE
		WHEN pvls.vl_result <= 0
		OR pvls.vl_result = 'LDL' THEN 'LDL'
		WHEN pvls.vl_result BETWEEN 1
		AND 400 THEN '1-400 Cpies'
		WHEN pvls.vl_result BETWEEN 401
		AND 999 THEN '401 - 999 Copies'
		WHEN pvls.vl_result >= 1000 THEN 'Above 1000 Copies'
		WHEN TO_DAYS(CURDATE()) - TO_DAYS(hv.visit_date) >= 180
		AND pvls.vl_result IS NULL
		AND CASE
			WHEN tx.visit_date IS NULL THEN 'Incative'
			ELSE 'On ART'
		END = 'On ART' THEN 'Due Not Bled'
		WHEN TO_DAYS(CURDATE()) - TO_DAYS(hv.visit_date) >= 180
		AND pvls.vl_result IS NULL
		AND CASE
			WHEN tx.visit_date IS NULL THEN 'Incative'
			ELSE 'On ART'
		END = 'Incative' THEN 'N/A'
		ELSE 'Not Due'
	END AS 'VLResults',
	CASE
		WHEN cx.visit_date between '2021-10-01'
		AND '2022-09-30'
		and cx.visit_date IS NOT NULL THEN 'Screened'
		else 'Not Screened'
	end as 'CaCx',
	monthname(cx.visit_date) as 'Last Visit Month'
FROM
	kenyaemr_etl.etl_hiv_enrollment hv
	LEFT JOIN kenyaemr_etl.etl_current_in_care tx ON hv.patient_id = tx.patient_id
	LEFT JOIN kenyaemr_etl.etl_patient_demographics pd ON pd.patient_id = hv.patient_id
	LEFT JOIN kenyaemr_etl.etl_contact co ON co.client_id = hv.patient_id
	LEFT JOIN kenyaemr_etl.etl_viral_load_tracker pvls ON pvls.patient_id = hv.patient_id
	LEFT JOIN kenyaemr_etl.etl_clinical_visit cv ON cv.client_id = hv.patient_id
	LEFT JOIN kenyaemr_etl.etl_cervical_cancer_screening cx on cx.patient_id = hv.patient_id
ORDER BY
	hv.visit_date,
	(
		CASE
			WHEN tx.visit_date IS NULL THEN 'Incative'
			ELSE 'On ART'
		END
	) DESC