import json
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def merge_applicant_and_recruiter_views():
    # Define the directories
    ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
    JSON_FOLDER_APP_VIEW = os.path.join(ROOT_DIR, "../data/jobs/fits_applicant_json")
    JSON_FOLDER_REC_VIEW = os.path.join(ROOT_DIR, "../data/jobs/fits_recruiter_json")
    JSON_FOLDER_MERGED = os.path.join(ROOT_DIR, "../data/jobs/fits_merged_json")

    # Check if directories exist and contain files
    if not os.path.exists(JSON_FOLDER_APP_VIEW) or not os.listdir(JSON_FOLDER_APP_VIEW):
        logging.error("The applicant view directory doesn't exist or is empty.")
        return
    if not os.path.exists(JSON_FOLDER_REC_VIEW) or not os.listdir(JSON_FOLDER_REC_VIEW):
        logging.error("The recruiter view directory doesn't exist or is empty.")
        return

    # Create the merged view directory if it doesn't exist
    if not os.path.exists(JSON_FOLDER_MERGED):
        os.makedirs(JSON_FOLDER_MERGED)

    logging.info("Starting to merge applicant and recruiter views.")
    logging.info(f"Total files to process: {len(os.listdir(JSON_FOLDER_APP_VIEW))}")

    # Iterate over each JSON file in the applicant view directory
    for filename in os.listdir(JSON_FOLDER_APP_VIEW):
        if filename.endswith(".json"):
            json_path_app_view = os.path.join(JSON_FOLDER_APP_VIEW, filename)
            json_path_rec_view = os.path.join(JSON_FOLDER_REC_VIEW, filename)
            json_path_merged = os.path.join(JSON_FOLDER_MERGED, filename)

            # Skip if corresponding recruiter view doesn't exist
            if not os.path.exists(json_path_rec_view):
                logging.info(f"Skipping {filename} because recruiter view doesn't exist.")
                continue

            # Load both views
            with open(json_path_app_view) as f:
                app_view = json.load(f)
            with open(json_path_rec_view) as f:
                rec_view = json.load(f)

            # Check if the necessary keys exist in the recruiter view
            if "fit_recruiter" not in rec_view or "fit_recruiter_detailed" not in rec_view:
                logging.error(f"Skipping {filename} because it does not contain necessary keys in the recruiter view.")
                continue

            # Merge the recruiter fields into the applicant view
            app_view["fit_recruiter"] = rec_view["fit_recruiter"]
            app_view["fit_recruiter_detailed"] = rec_view["fit_recruiter_detailed"]


            # Store the merged view
            with open(json_path_merged, "w") as f:
                json.dump(app_view, f, indent=4)

            logging.info(f"Successfully merged and stored view for {filename}.")

    logging.info("Finished merging applicant and recruiter views.")

if __name__ == "__main__":
    merge_applicant_and_recruiter_views()

