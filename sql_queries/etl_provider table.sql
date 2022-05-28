INSERT INTO
    kenyaemr_etl.etl_provider (
        SELECT
            p.identifier AS 'Creator id',
            UPPER(concat(pd.given_name, ' ', pd.family_name))
        FROM
            openmrs.provider p
            JOIN kenyaemr_etl.etl_patient_demographics pd ON pd.patient_id = p.person_id
        ORDER BY
            concat(pd.given_name, ' ', pd.family_name)
    )