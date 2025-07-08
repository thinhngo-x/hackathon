# Vultr Deployment Documentation

## 🚀 Quick Deploy to Vultr

We've created several deployment options for your Ticket Assistant on Vultr:

### Option 1: One-Click Deploy (Recommended)

```bash
./scripts/quick-deploy.sh
```

### Option 2: Manual Single Instance

```bash
chmod +x scripts/deploy-vultr.sh
export VULTR_API_KEY=your_api_key_here
./scripts/deploy-vultr.sh
```

### Option 3: Kubernetes Deployment

```bash
chmod +x scripts/deploy-vultr-k8s.sh
export VULTR_API_KEY=your_api_key_here
./scripts/deploy-vultr-k8s.sh
```

## 📋 Prerequisites

1. **Vultr API Key**: Get from https://my.vultr.com/settings/#settingsapi
2. **Groq API Key** (optional): Get from https://console.groq.com/keys
3. **Docker**: Install from https://docs.docker.com/get-docker/
4. **Docker Compose**: Usually included with Docker

## 🔧 Deployment Options

### Single Instance ($10/month)

- 1 CPU, 2GB RAM
- Simple deployment
- Good for demos/testing
- Automatic SSL with Let's Encrypt

### Kubernetes Cluster ($20/month)

- 2 worker nodes
- Auto-scaling
- Production-ready
- Load balancing

## 🌍 Available Regions

- **ewr** (New York) - Default
- **ord** (Chicago)
- **dfw** (Dallas)
- **sea** (Seattle)
- **lax** (Los Angeles)
- **atl** (Atlanta)
- **mia** (Miami)
- **lhr** (London)
- **ams** (Amsterdam)
- **fra** (Frankfurt)
- **nrt** (Tokyo)
- **sgp** (Singapore)
- **syd** (Sydney)

## 🔐 Security Features

- Automatic firewall configuration
- SSL/TLS termination
- Private networking
- API key protection
- Health checks

## 📊 Monitoring

After deployment, you can monitor your application:

```bash
# Check instance status
vultr-cli instance get YOUR_INSTANCE_ID

# View application logs
ssh root@YOUR_INSTANCE_IP 'cd /opt/ticket-assistant && docker-compose logs'

# Check health
curl http://YOUR_INSTANCE_IP/health
```

## 🔄 Updates

To update your deployed application:

```bash
# Option 1: Re-run deployment script
./scripts/deploy-vultr.sh

# Option 2: Manual update
git pull origin main
scp -r . root@YOUR_INSTANCE_IP:/opt/ticket-assistant/
ssh root@YOUR_INSTANCE_IP 'cd /opt/ticket-assistant && docker-compose up -d --build'
```

## 💰 Cost Estimation

### Single Instance Deployment

- Vultr Cloud Compute: $10/month
- Bandwidth: $0.01/GB
- Total: ~$12/month

### Kubernetes Deployment

- VKE Control Plane: Free
- 2x Worker Nodes: $20/month
- Load Balancer: $10/month
- Total: ~$30/month

## 🔍 Troubleshooting

### Common Issues

1. **API Key Not Working**

   ```bash
   # Test your API key
   curl -H "Authorization: Bearer $VULTR_API_KEY" https://api.vultr.com/v2/account
   ```

2. **Instance Not Starting**

   ```bash
   # Check instance status
   vultr-cli instance get YOUR_INSTANCE_ID
   ```

3. **Application Not Responding**
   ```bash
   # Check Docker containers
   ssh root@YOUR_INSTANCE_IP 'docker ps'
   ssh root@YOUR_INSTANCE_IP 'docker-compose logs'
   ```

### Support

- 📧 Vultr Support: https://www.vultr.com/support/
- 📚 Documentation: https://www.vultr.com/docs/
- 💬 Community: https://www.vultr.com/community/

## 🎯 Production Checklist

Before going live:

- [ ] Custom domain configured
- [ ] SSL certificate installed
- [ ] Environment variables secured
- [ ] Monitoring setup
- [ ] Backup strategy
- [ ] Scaling plan
- [ ] Load testing completed

## 🔗 Useful Links

- [Vultr API Documentation](https://www.vultr.com/api/)
- [Vultr CLI Documentation](https://github.com/vultr/vultr-cli)
- [Kubernetes on Vultr](https://www.vultr.com/kubernetes/)
- [Vultr Marketplace](https://www.vultr.com/marketplace/)

---

Happy deploying! 🚀
