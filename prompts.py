TRF_EXTRACTION_PROMPT = """
Extract the handwritten print under each respected field.

For every field, carefully distinguish between three possible situations. First, the field may be genuinely blank, meaning nothing was written, marked, or signed by the patient or physician. In this case, set the field's value to the exact word 'blank' and give it a high confidence score, since you are certain nothing is there. Second, something may be written or marked but it is difficult to read clearly, such as messy handwriting or a faint checkbox. In this case, provide your best interpretation of the value and give it a low confidence score below 0.9, so it can be flagged for review. Third, something may be present but visually subtle and easy to overlook, such as a light pencil checkmark or a faint signature. Examine every field closely, including checkboxes and signature lines, before concluding a field is blank. Do not report a field as 'blank' unless you have carefully confirmed there is truly nothing marked there. If you are uncertain whether a faint mark exists, treat it as present but unclear, and report it with a low confidence score rather than marking it blank.

CRITICAL WARNING about Sex at Birth: this field is frequently misread. You must look at this specific checkbox in complete isolation from any other information on the form, including the patient's name. Do NOT use the patient's name, any other field, or any assumption to decide this value. Look ONLY at whether the M circle or the F circle has an actual ink or pencil mark inside it. If you see no mark in either circle, the answer is 'blank' — this is the most common correct answer for this field, not an exception. Getting this field wrong is a serious clinical error. Triple-check this specific field before finalizing your answer.

For checkbox and selection fields specifically (such as Sex at Birth, Race, Ethnicity, Billing Type), only report a value if a mark is clearly and visibly present in that specific box. Never infer or guess a selection based on what is typical or common. If you cannot clearly see a mark in any box for a given field, you must report the value as 'blank', even if only one reasonable option exists.

If any text on the form appears crossed out, struck through, or scribbled over, treat that text as invalid and do not use it as the field's value. If corrected or replacement text is written near the crossed-out text, use that replacement text instead. If no replacement text is present, report the field's value as 'blank'.

Each field is contained in its own labeled box on the form. Do not combine text from adjacent fields into one value, even if the handwriting appears to overlap or extend near another field's boundary. If a value seems to contain content clearly meant for a different labeled field, only extract the portion that belongs to the current field's label.

Ordering Physician Information: Practice/Client Name, Phone, Last Name, First Name, NPI #, Email, Fax, Street Address, City, State, Postal Code.

Patient Information: Last Name Required, First Name Required, MI, Date Of Birth (MM/DD/YYYY), Phone, Sex at Birth (this is a checkmark of either M or F, it is not free text), Email (for online report access), Medical Record #, Street Address/PO Box/Building/Floor/etc, City, State/Province/Region, Zip/Postal Code, Country. Check which box is checked off; whichever has the majority mark is the one selected, there can only be one.

Demographic: Race: White, Asian, Black/African American, Native America/Alaska Native, Native Hawaiian/Other Pacific Islander. Ethnicity: Not Hispanic, Latino, Spanish OR Hispanic, Latino, Spanish.

Patient History: Diabetes AND/OR Family of MI Z82.49, Family History of Heart Attack, Stroke, Coronary Artery Bypass, Stent or Angina, <= 65 years of age (Parent/sibling/child) AND/OR High Dose Biotin. This field will be a checkbox, so look for a mark.

Billing Information: Client OR Patient Self-Pay. This field will be a checkmark, so look for which option is checked.

Test Requested: 1003 SmartVascular DX (SVDx) OR 1028 Expanded Lipid Profile (ELP) OR 1003/1028 SmartVascular DX and ELP Panel. This field will be a checkmark, so look for which test is checked.

Specimen Collection: Date Collected in MM/DD/YYYY, Time (AM or PM marked), Collected by (please print).

Ordering Physician Signature/Attestation: Just note if a signature is there, then say 'Signature collected'; if not, say 'Signature not collected'. Date in MM/DD/YYYY.

Patient Acknowledgment: This has a checkmark option, but also writing. Just note if a signature is there, then say 'Signature collected'; if not, say 'Signature not collected'. Date in MM/DD/YYYY.

Once carefully extracting all fields specified, return all extracted data as a structured JSON object using these extracted field names, and include a confidence score between 0 and 1 for each field. Keep all original fields and values in the main structured JSON as specified above. Use lowercase snake_case field names as the JSON keys. Use the following exact field mapping. Do not invent your own key names — match each field to the exact key listed below.

Ordering Physician Information:
Practice/Client Name -> practice_client_name
Phone (in this section) -> ordering_physician_phone
Last Name (in this section) -> ordering_physician_last_name
First Name (in this section) -> ordering_physician_first_name
NPI # -> npi
Email (in this section) -> ordering_physician_email
Fax -> ordering_physician_fax
Street Address (in this section) -> ordering_physician_street_address
City (in this section) -> ordering_physician_city
State (in this section) -> ordering_physician_state
Postal Code -> ordering_physician_postal_code

Patient Information:
Last Name Required -> patient_last_name
First Name Required -> patient_first_name
MI -> patient_middle_initial
Date of Birth (MM/DD/YYYY) -> date_of_birth
Phone (in this section) -> patient_phone
Sex at Birth -> sex_at_birth
Email (for online report access) -> patient_email
Medical Record # -> medical_record_number
Street Address/PO Box/Building/Floor/etc -> patient_street_address
City (in this section) -> patient_city
State/Province/Region -> patient_state
Zip/Postal Code -> patient_zip_code
Country -> patient_country

Demographic:
Race (selected option only) -> race
Ethnicity (selected option only) -> ethnicity

Patient History:
Diabetes checkbox -> patient_history_diabetes
Family of MI Z82.49 / Family History checkbox -> patient_history_family_heart
High Dose Biotin checkbox -> patient_history_high_dose_biotin

Billing Information:
Client OR Patient Self-Pay (selected option) -> billing_type

Test Requested:
The single selected test option -> test_requested

Specimen Collection:
Date Collected -> specimen_collection_date
Time (AM or PM) -> specimen_collection_time
Collected by -> specimen_collected_by

Ordering Physician Signature/Attestation section:
Signature presence -> ordering_physician_signature_status (value must be exactly 'Signature collected' or 'Signature not collected')
Date (in this section) -> ordering_physician_date

Patient Acknowledgment section:
Signature presence -> patient_acknowledgment_signature_status (value must be exactly 'Signature collected' or 'Signature not collected')
Date (in this section) -> patient_acknowledgment_date

This form contains three separate date fields in different sections that must not be confused with one another. Name the date field in the Ordering Physician signature section exactly 'ordering_physician_date'. Name the date field in the Patient Acknowledgment signature section exactly 'patient_acknowledgment_date'. Name the date field in the Specimen Collection section exactly 'specimen_collection_date'. Do not use the generic key 'date' for any of these three fields.

Return your response as JSON matching exactly this structure:

{
  "extracted_fields": {
    "practice_client_name": {"value": "...", "confidence": 0.0},
    "ordering_physician_phone": {"value": "...", "confidence": 0.0}
  },
  "low_confidence_fields": [
    {"field_name": "npi", "value": "...", "confidence": 0.0, "reason": "..."}
  ]
}

Every field in extracted_fields must follow the {"value": ..., "confidence": ...} shape.
low_confidence_fields must be a LIST of objects, each containing field_name, value, confidence, and reason.
Include every field listed in the mapping above in extracted_fields, even if the value is "blank".
"""