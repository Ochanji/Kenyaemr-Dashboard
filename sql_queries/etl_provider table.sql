USE kenyaemr_etl;
DROP TABLE IF EXISTS etl_provider;
CREATE TABLE etl_provider (creator_id VARCHAR(50), provider VARCHAR(50));
INSERT INTO
    kenyaemr_etl.etl_provider (
        SELECT
            p.identifier AS 'Creator id',
            UPPER(concat(pd.given_name, ' ', pd.family_name))
        FROM
            openrms.provider p
            JOIN kenyaemr_etl.etl_patient_demographics pd ON pd.patient_id = p.person_id
        ORDER BY
            concat(pd.given_name, ' ', pd.family_name)
    )