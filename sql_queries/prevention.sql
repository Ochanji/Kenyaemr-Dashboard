SELECT
	DISTINCT UPPER(p.provider) AS 'Provider',
	cv.visit_date AS 'Date',
	CASE
		WHEN cv.visit_date BETWEEN '2016-10-01'
		AND '2017-09-30' THEN 'Steps_FY1'
		WHEN cv.visit_date BETWEEN '2017-10-01'
		AND '2018-09-30' THEN 'Steps_FY2'
		WHEN cv.visit_date BETWEEN '2018-10-01'
		AND '2019-09-30' THEN 'Steps_FY3'
		WHEN cv.visit_date BETWEEN '2019-10-01'
		AND '2020-09-30' THEN 'Steps_FY4'
		WHEN cv.visit_date BETWEEN '2020-10-01'
		AND '2021-09-30' THEN 'Steps_FY5'
		WHEN cv.visit_date BETWEEN '2021-10-01'
		AND '2022-09-30' THEN 'Vukisha_FY1'
		WHEN cv.visit_date BETWEEN '2022-10-01'
		AND '2023-09-30' THEN 'Vukisha_FY2'
		WHEN cv.visit_date BETWEEN '2023-10-01'
		AND '2024-09-30' THEN 'Vukisha_FY3'
		WHEN cv.visit_date BETWEEN '2024-10-01'
		AND '2025-09-30' THEN 'Vukisha_FY4'
		WHEN cv.visit_date BETWEEN '2025-10-01'
		AND '2026-09-30' THEN 'Vukisha_FY5'
	END AS 'Financial_Year',
	MONTHNAME(cv.visit_date) AS 'Month',
	UPPER(pd.given_name) AS 'First Name',
	UPPER(pd.middle_name) AS 'Middle Name',
	UPPER(pd.family_name) AS 'Last Name',
	pd.gender AS 'Gender',
	YEAR(CURDATE()) - YEAR(pd.dob) AS 'Age',
	CASE
		WHEN co.unique_identifier LIKE '%45266%' THEN 'Nyaribari Masaba'
		WHEN co.unique_identifier LIKE '%45262%' THEN 'South Mugirango'
		WHEN co.unique_identifier LIKE '%45264%' THEN 'Bobasi'
		WHEN co.unique_identifier LIKE '%45261%' THEN 'Bonchari'
		WHEN co.unique_identifier LIKE '%45269%' THEN 'Kitutu Chache South'
		ELSE 'Unknown'
	END AS 'Sub_County',
	CASE
		WHEN co.key_population_type = 'MSW' THEN 'MSM'
		WHEN co.key_population_type = 'Transgender' THEN 'TG'
		ELSE co.key_population_type
	END AS 'KPType',
	CASE
		WHEN cv.type_of_visit IS NULL THEN 'NA'
		ELSE cv.type_of_visit
	END AS 'Type_Of_Visit',
	CASE
		WHEN cv.violence_results != 'Rape/Sexual assault' THEN 'Physical/Emotional'
		WHEN cv.violence_results IS NULL THEN 'N/A'
		ELSE 'Rape/Sexual assault'
	END AS 'GBV',
	CASE
		WHEN tst.visit_date is not null then 'Tested'
		else 'Not Tested'
	end as 'HIV Test',
	case
		when case
			WHEN tst.visit_date is not null then 'Tested'
			else 'Not Tested'
		end = 'Tested' then tst.final_test_result
		else ''
	end as 'HIV Result',
	case
		when tst.final_test_result = 'Positive'
		OR he.visit_date is not null then 'HIV Positive'
		else 'HIV Negative'
	end as 'HIV Status',
	case
		when cx.visit_date between '2021-10-01'
		and '2022-09-30'
		and cx.visit_date is not null
		and pd.Gender != 'M' THEN 'Screened'
		else ''
	end as 'CaCx'
FROM
	kenyaemr_etl.etl_clinical_visit cv
	JOIN kenyaemr_etl.etl_patient_demographics pd ON pd.patient_id = cv.client_id
	LEFT JOIN kenyaemr_etl.etl_contact co ON co.client_id = cv.client_id
	LEFT JOIN kenyaemr_etl.etl_provider p ON p.creator_id = cv.encounter_provider
	LEFT JOIN kenyaemr_etl.etl_hts_test tst ON tst.patient_id = cv.client_id
	and tst.visit_id = cv.visit_id
	LEFT JOIN kenyaemr_etl.etl_cervical_cancer_screening cx on cx.patient_id = cv.client_id
	and cx.visit_id = cv.visit_id
	LEFT JOIN kenyaemr_etl.etl_hiv_enrollment he on he.patient_id = cv.client_id
WHERE
	co.key_population_type IS NOT NULL
	AND CASE
		WHEN cv.visit_date BETWEEN '2016-10-01'
		AND '2017-09-30' THEN 'Steps_FY1'
		WHEN cv.visit_date BETWEEN '2017-10-01'
		AND '2018-09-30' THEN 'Steps_FY2'
		WHEN cv.visit_date BETWEEN '2018-10-01'
		AND '2019-09-30' THEN 'Steps_FY3'
		WHEN cv.visit_date BETWEEN '2019-10-01'
		AND '2020-09-30' THEN 'Steps_FY4'
		WHEN cv.visit_date BETWEEN '2020-10-01'
		AND '2021-09-30' THEN 'Steps_FY5'
		WHEN cv.visit_date BETWEEN '2021-10-01'
		AND '2022-09-30' THEN 'Vukisha_FY1'
		WHEN cv.visit_date BETWEEN '2022-10-01'
		AND '2023-09-30' THEN 'Vukisha_FY2'
		WHEN cv.visit_date BETWEEN '2023-10-01'
		AND '2024-09-30' THEN 'Vukisha_FY3'
		WHEN cv.visit_date BETWEEN '2024-10-01'
		AND '2025-09-30' THEN 'Vukisha_FY4'
		WHEN cv.visit_date BETWEEN '2025-10-01'
		AND '2026-09-30' THEN 'Vukisha_FY5'
	END IS NOT NULL;