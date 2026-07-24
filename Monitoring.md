I’m narrowing this to a clear monitoring and observability summary with concrete “done now” versus “next steps” points.

## Monitoring and Observability

Here is a clear way to present that part.

### What is already done
- The application has basic health endpoints:
  - /health
  - /ready
  - /version
- The app logs request and response activity in app.py
- Kubernetes probes are configured in deployment.yaml for:
  - liveness
  - readiness
- The deployment has basic resource limits and requests in the Helm values and chart
- CI/CD pipelines provide visibility into build, test, and deployment status through GitHub Actions
- “Currently, logs can be viewed from the application console locally and from Kubernetes pod logs in the cluster using kubectl.”
As of now in this project:

The readiness endpoint helps ensure the app is actually usable before traffic is routed to it.
The liveness endpoint helps detect a non-responsive app and recover it automatically.
They are part of the basic reliability setup in deployment.yaml.

### What this gives you today
- You can tell if the service is up or down
- You can see whether pods are becoming ready
- You can inspect basic app logs for request activity
- You can track whether deployments are succeeding or failing

## Deployment steps for Prometheus and Grafana

1. Deploy the Flask application chart:
   - `helm install flask-app ./helm/flask-app`
2. Deploy the monitoring stack:
   - `helm install monitoring ./helm/monitoring`
3. Check the services:
   - `kubectl get svc`
4. Open the dashboards:
   - Prometheus: `http://<external-ip>:9090`
   - Grafana: `http://<external-ip>:3000`
5. Log in to Grafana with:
   - Username: `admin`
   - Password: `admin`

> The Flask app now exposes a `/metrics` endpoint that Prometheus can scrape automatically when the monitoring stack is installed.

Flask app: http://<external-ip>:5000/
Health endpoint: http://<external-ip>:5000/health
Other URLs:

Grafana: http://<external-ip>:3000
Prometheus: http://<external-ip>:9090
