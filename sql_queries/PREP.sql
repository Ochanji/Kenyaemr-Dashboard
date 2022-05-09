SELECT
	DISTINCT UPPER(COALESCE(p.provider, 'NA')) AS 'Provider',
	monthname(pe.visit_date) as 'Month',
	pe.visit_date AS 'Date Started on PrEP',
	CASE
		WHEN pe.visit_date BETWEEN '2016-10-01'
		AND '2017-09-30' THEN 'Steps_FY1'
		WHEN pe.visit_date BETWEEN '2017-10-01'
		AND '2018-09-30' THEN 'Steps_FY2'
		WHEN pe.visit_date BETWEEN '2018-10-01'
		AND '2019-09-30' THEN 'Steps_FY3'
		WHEN pe.visit_date BETWEEN '2019-10-01'
		AND '2020-09-30' THEN 'Steps_FY4'
		WHEN pe.visit_date BETWEEN '2020-10-01'
		AND '2021-09-30' THEN 'Steps_FY5'
		WHEN pe.visit_date BETWEEN '2021-10-01'
		AND '2022-09-30' THEN 'Vukisha_FY1'
		WHEN pe.visit_date BETWEEN '2022-10-01'
		AND '2023-09-30' THEN 'Vukisha_FY2'
		WHEN pe.visit_date BETWEEN '2023-10-01'
		AND '2024-09-30' THEN 'Vukisha_FY3'
		WHEN pe.visit_date BETWEEN '2024-10-01'
		AND '2025-09-30' THEN 'Vukisha_FY4'
		WHEN pe.visit_date BETWEEN '2025-10-01'
		AND '2026-09-30' THEN 'Vukisha_FY5'
	END AS 'Financial_Year',
	CASE
		WHEN CASE
			WHEN co.key_population_type IS NULL THEN 'General Population'
			ELSE co.key_population_type
		END = 'General Population' THEN 'General Population'
		ELSE 'KeyPopulation'
	END AS 'PopulationType',
	case
		when co.key_population_type is null then 'General Population'
		when co.key_population_type = 'MSW' then 'MSM'
		when co.key_population_type = 'Transgender' then 'TG'
		ELSE co.key_population_type
	end as 'KPType',
	CASE
		WHEN pe.visit_date IS NOT NULL THEN 'Prep New'
		ELSE ''
	END AS 'PrepNew',
	pd.given_name AS 'First Name',
	pd.middle_name AS 'Middle Name',
	pd.family_name AS 'Last Name',
	pd.Gender AS 'Gender',
	YEAR(CURDATE()) - YEAR(pd.dob) AS 'Age'
FROM
	kenyaemr_etl.etl_prep_enrolment pe
	LEFT JOIN kenyaemr_etl.etl_hts_test tst ON tst.patient_id = pe.patient_id
	AND tst.visit_id = pe.visit_id
	JOIN kenyaemr_etl.etl_patient_demographics pd ON pd.patient_id = pe.patient_id
	LEFT JOIN kenyaemr_etl.etl_provider p ON p.creator_id = tst.creator
	LEFT JOIN kenyaemr_etl.etl_contact co ON co.client_id = pe.patient_id