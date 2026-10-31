# Dental Cavity Detection: trained image classifier

Source: Caries-Spectra V2, Himel, Islam and Hannan, DOI 10.17632/9jnf2jvghy.2, CC BY 4.0.
Original source and changes are recorded in source_information/ and dataset_summary.json.

Use the complete dental_caries.keras model or dental_caries_saved_model for predictions.
Input: RGB float32, 0..255. Resizing to 224x224 and scaling to [-1,1] are embedded.
Do not normalize to 0..1 before inference. Class order is in class_names.json.
Run: python predict.py your-image.jpg after installing requirements_inference.txt.

metrics.json and test_predictions.csv contain measured results from this training run.
The partition groups visually similar images; patient independence is not established.
The labels identify image-level enamel caries categories, not cavity boxes or masks.
Early enamel caries does not necessarily indicate a visible cavity.
A no-enamel-caries label does not mean absence of all dental conditions.
This is an educational prototype, not a clinically validated diagnostic system.
