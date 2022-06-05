SELECT DISTINCT
    pf.patient_id,
    pe.visit_date AS 'Date Enroled',
    pf.visit_date AS 'Follow-Up',
    tst.visit_date AS 'Date Test',
    tst.final_test_result 'HTSResult',
    pf.treatment_plan,
    CASE
        WHEN - TO_DAYS(CURDATE()) + TO_DAYS(pf.appointment_date) > - 7 THEN 'Active'
    END AS 'Status',
    pf.appointment_date AS TCA
FROM
    kenyaemr_etl.etl_prep_followup pf
        LEFT JOIN
    kenyaemr_etl.etl_patient_demographics pd ON pd.patient_id = pf.patient_id
        LEFT JOIN
    kenyaemr_etl.etl_contact co ON co.client_id = pf.patient_id
        LEFT JOIN
    kenyaemr_etl.etl_prep_enrolment pe ON pe.patient_id = pf.patient_id
        LEFT JOIN
    kenyaemr_etl.etl_hts_test tst ON tst.patient_id = pf.patient_id
        AND tst.visit_id = pf.visit_id
WHERE
    CASE
        WHEN - TO_DAYS(CURDATE()) + TO_DAYS(pf.appointment_date) > - 7 THEN 'Active'
    END = 'Active'
        AND pf.treatment_plan != 'Start'