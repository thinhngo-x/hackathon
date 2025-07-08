# 🚀 Deploy to Vultr Cloud

## Quick Start

1. **Setup prerequisites**:

   ```bash
   ./scripts/setup-vultr.sh
   ```

2. **Get your API keys**:

   - Vultr API Key: https://my.vultr.com/settings/#settingsapi
   - Groq API Key (optional): https://console.groq.com/keys

3. **Deploy with one command**:
   ```bash
   ./scripts/quick-deploy.sh
   ```

## Manual Deployment

### Option 1: Single Instance ($10/month)

```bash
export VULTR_API_KEY="your_vultr_api_key_here"
export GROQ_API_KEY="your_groq_api_key_here"  # Optional
./scripts/deploy-vultr.sh
```

### Option 2: Kubernetes Cluster ($30/month)

```bash
export VULTR_API_KEY="your_vultr_api_key_here"
export GROQ_API_KEY="your_groq_api_key_here"  # Optional
./scripts/deploy-vultr-k8s.sh
```

## What Gets Deployed

- **Backend**: FastAPI with AI-powered ticket classification
- **Frontend**: React + Vite with modern UI
- **Database**: SQLite (upgradeable to PostgreSQL)
- **Reverse Proxy**: Nginx with SSL termination
- **Monitoring**: Health checks and logging

## Post-Deployment

After deployment, you'll get:

- 🌐 **Frontend URL**: `http://your-instance-ip`
- 📚 **API Documentation**: `http://your-instance-ip/docs`
- 🔧 **SSH Access**: `ssh root@your-instance-ip`

## Scaling

- **Horizontal**: Add more instances behind load balancer
- **Vertical**: Upgrade instance size
- **Auto-scaling**: Use Kubernetes deployment

## Support

- 📖 Full documentation: [VULTR_DEPLOY.md](VULTR_DEPLOY.md)
- 🆘 Issues: Create GitHub issue
- 💬 Community: Vultr Discord

---

**Ready to deploy? Start with**: `./scripts/quick-deploy.sh`
