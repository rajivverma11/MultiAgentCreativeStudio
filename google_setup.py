# ============================================================
# GOOGLE CLOUD CLI + VERTEX AI — LOCAL MAC SETUP
# ============================================================


# 1. Install Google Cloud CLI using Homebrew
#brew install --cask google-cloud-sdk


# 2. Restart the shell after installation
#exec zsh


# 3. Verify that gcloud is installed
#gcloud --version


# 4. Log into your Google Cloud account
#gcloud auth login


# 5. Create Application Default Credentials (ADC)
# IMPORTANT for Python, Google ADK, Vertex AI, etc.
#gcloud auth application-default login


# 6. List the Google Cloud projects you have access to
#gcloud projects list


# 7. Set the project you want to use
# Replace YOUR_PROJECT_ID with your actual project ID
#gcloud config set project YOUR_PROJECT_ID


# 8. Verify which project is currently selected
#gcloud config get-value project


# 9. Get the project's numeric Project Number
#gcloud projects describe YOUR_PROJECT_ID \
 # --format="value(projectNumber)"


# 10. Enable the Vertex AI API
#gcloud services enable aiplatform.googleapis.com


# 11. Verify that the Vertex AI API is enabled
#gcloud services list --enabled \
  #--filter="name:aiplatform.googleapis.com"



# gcloud auth login
#         ↓
# Authenticates YOU for the gcloud command-line tool

# gcloud auth application-default login
#         ↓
# Authenticates your LOCAL APPLICATIONS
# (Python / Google ADK / Vertex AI SDK)

# For the work you're doing with Google ADK, the second one—gcloud auth application-default login—is particularly important because '
# 'that's how your local Python application obtains credentials to call Vertex AI.
# You don't need to repeat all of these every time you work. Normally, after the initial '
# 'setup, you can simply activate your Python environment and work. You'd revisit these commands when setting up 
# a new computer, switching GCP projects/accounts, or if your local Google credentials need to be refreshed.