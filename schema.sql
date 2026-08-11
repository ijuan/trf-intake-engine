-- TRF Intake Engine — database schema
-- Fresh setup:  mysql -u root -p < schema.sql

CREATE DATABASE IF NOT EXISTS trf_intake_engine;
USE trf_intake_engine;

CREATE TABLE extracted_data (
    form_id INT AUTO_INCREMENT PRIMARY KEY,
    practice_client_name VARCHAR(255),
    ordering_physician_phone VARCHAR(255),
    ordering_physician_last_name VARCHAR(255),
    ordering_physician_first_name VARCHAR(255),
    npi VARCHAR(255),
    ordering_physician_email VARCHAR(255),
    ordering_physician_fax VARCHAR(255),
    ordering_physician_street_address VARCHAR(255),
    ordering_physician_building_number VARCHAR(255),
    ordering_physician_city VARCHAR(255),
    ordering_physician_state VARCHAR(255),
    ordering_physician_postal_code VARCHAR(255),
    patient_last_name VARCHAR(255),
    patient_first_name VARCHAR(255),
    patient_middle_initial VARCHAR(255),
    date_of_birth DATE,
    patient_phone VARCHAR(255),
    sex_at_birth VARCHAR(255),
    patient_email VARCHAR(255),
    medical_record_number VARCHAR(255),
    patient_street_address VARCHAR(255),
    patient_city VARCHAR(255),
    patient_state VARCHAR(255),
    patient_zip_code VARCHAR(255),
    patient_country VARCHAR(255),
    race VARCHAR(255),
    ethnicity VARCHAR(255),
    patient_history_diabetes VARCHAR(255),
    patient_history_family_heart VARCHAR(255),
    patient_history_high_dose_biotin VARCHAR(255),
    billing_type VARCHAR(255),
    test_requested VARCHAR(255),
    specimen_collection_date DATE,
    specimen_collection_time VARCHAR(255),
    specimen_collected_by VARCHAR(255),
    ordering_physician_signature_status VARCHAR(255),
    ordering_physician_date DATE,
    patient_acknowledgment_signature_status VARCHAR(255),
    patient_acknowledgment_date DATE,
    icd10_other VARCHAR(255)
);

CREATE TABLE icd10_codes (
    form_id INT,
    code VARCHAR(255),
    FOREIGN KEY (form_id) REFERENCES extracted_data(form_id)
);

CREATE TABLE flagged_fields (
    form_id INT,
    flagged_field VARCHAR(255),
    form_1_value VARCHAR(255),
    form_2_value VARCHAR(255),
    FOREIGN KEY (form_id) REFERENCES extracted_data(form_id)
);
