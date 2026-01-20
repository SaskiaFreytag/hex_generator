# Hex Generator Slack Command

This service exposes a Slack slash command handler at `POST /slack/hex` and generates hex codes.

## Deploy on Google Cloud Run

### 1) Build and push the container image

From the repo root, use Cloud Build to build and push the container image:

```bash
gcloud builds submit --tag gcr.io/PROJECT_ID/hex-generator
```

Replace `PROJECT_ID` with your Google Cloud project ID.

### 2) Deploy to Cloud Run

```bash
gcloud run deploy hex-generator \
  --image gcr.io/PROJECT_ID/hex-generator \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars SLACK_SIGNING_SECRET=your_signing_secret
```

Cloud Run expects the service to listen on port `8080`, which is configured in `slack_app.py` and
exposed in the Dockerfile.

### 3) Configure Slack

Set your Slash Command Request URL to:

```
https://YOUR_CLOUD_RUN_URL/slack/hex
```

## Cost expectations (very low traffic)

With ~35 users and ~0.1 requests per user per day on weekdays, that is roughly:

```
35 users × 0.1 requests/day × 5 days/week ≈ 17.5 requests/week
```

That traffic is extremely low and should typically fit within Cloud Run’s free tier for requests and
CPU/memory time. Actual costs vary by region and resource settings, so check the Google Cloud
pricing calculator for exact numbers before deployment.

## Troubleshooting: Cloud Build permission denied

If you see:

```
ERROR: (gcloud.builds.submit) PERMISSION_DENIED: The caller does not have permission.
```

This usually means the active `gcloud` account does not have access to the target project. Fix it by
making sure the **same Google account** has access to the project you’re building in:

1. Check which account is active:

   ```bash
   gcloud auth list
   ```

2. Switch to the account that has access to the project (or add that account to the project in
   **IAM & Admin**):

   ```bash
   gcloud auth login
   ```

3. Make sure you are targeting the correct project ID:

   ```bash
   gcloud config set project PROJECT_ID
   ```

Your GitHub account does not affect Google Cloud permissions; access is controlled by the Google
account you use with `gcloud`. Ensure that account has at least **Cloud Build Editor** and **Storage
Admin** roles (or equivalent) for the project.
