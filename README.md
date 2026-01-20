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
