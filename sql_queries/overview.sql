SELECT
	DISTINCT CASE
		WHEN co.unique_identifier LIKE '%45266%' THEN 'Nyaribari Masaba'
		WHEN co.unique_identifier LIKE '%45262%' THEN 'South Mugirango'
		WHEN co.unique_identifier LIKE '%45264%' THEN 'Bobasi'
		WHEN co.unique_identifier LIKE '%45261%' THEN 'Bonchari'
		WHEN co.unique_identifier LIKE '%45269%' THEN 'Kitutu Chache South'
		ELSE 'Unknown'
	END AS 'Sub_County',
	pd.given_name AS 'First Name',
	pd.middle_name AS 'Middle Name',
	pd.family_name AS 'Last Name',
	YEAR(CURDATE()) - YEAR(pd.dob) AS Age,
	pd.Gender AS 'Gender',
	CASE
		WHEN co.visit_date IS NOT NULL
		AND hv.visit_date IS NULL THEN 'Prevention'
		WHEN hv.visit_date IS NOT NULL
		AND co.visit_date IS NOT NULL THEN 'HIV C&T'
		ELSE 'GP Not Enrolled'
	END AS 'Program',
	CASE
		WHEN co.visit_date IS NULL THEN 'GenPOP'
		ELSE 'KeyPOP'
	END AS 'Population Type',
	CASE
		WHEN co.key_population_type = 'MSW' THEN 'MSM'
		WHEN co.key_population_type = 'Transgender' THEN 'TG'
		WHEN co.key_population_type IS NULL THEN 'Unknown'
		ELSE co.key_population_type
	END AS 'KPType'
FROM
	kenyaemr_etl.etl_patient_demographics AS pd
	LEFT JOIN kenyaemr_etl.etl_current_in_care AS tx_curr ON tx_curr.patient_id = pd.patient_id
	LEFT JOIN kenyaemr_etl.etl_contact co ON co.client_id = pd.patient_id
	LEFT JOIN kenyaemr_etl.etl_clinical_visit cv ON cv.client_id = pd.patient_id
	LEFT JOIN kenyaemr_etl.etl_hiv_enrollment hv ON hv.patient_id = pd.patient_id
WHERE
	pd.Gender != 'U'
	AND YEAR(CURDATE()) - YEAR(pd.dob) >= 1;