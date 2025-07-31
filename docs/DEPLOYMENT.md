# 🚀 Deployment Guide

This guide covers deploying your VRP Algorithm Demo to various platforms.

## 📋 Prerequisites

- Python 3.11+
- Git repository with your code
- Account on your chosen deployment platform

## 🎯 Deployment Options

### 1. Streamlit Cloud (Recommended)

**Easiest deployment option for Streamlit apps**

1. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud**:
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select your repository
   - Set the path to your app: `src/python/streamlit_vrp_app.py`
   - Click "Deploy"

3. **Your app will be live** at `https://your-app-name.streamlit.app`

### 2. Heroku

**Traditional cloud platform**

1. **Install Heroku CLI**:
   ```bash
   # macOS
   brew install heroku/brew/heroku
   
   # Windows
   # Download from https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Login to Heroku**:
   ```bash
   heroku login
   ```

3. **Create Heroku app**:
   ```bash
   heroku create your-vrp-app-name
   ```

4. **Deploy**:
   ```bash
   git push heroku main
   ```

5. **Open your app**:
   ```bash
   heroku open
   ```

### 3. Railway

**Modern deployment platform**

1. **Go to [railway.app](https://railway.app)**
2. **Sign in with GitHub**
3. **Click "New Project"**
4. **Select "Deploy from GitHub repo"**
5. **Select your repository**
6. **Railway will automatically detect and deploy**

### 4. Render

**Free tier available**

1. **Go to [render.com](https://render.com)**
2. **Sign up and connect GitHub**
3. **Click "New Web Service"**
4. **Select your repository**
5. **Configure**:
   - **Name**: `vrp-algorithm-demo`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run src/python/streamlit_vrp_app.py --server.port $PORT --server.address 0.0.0.0`
6. **Click "Create Web Service"**

## 🔧 Configuration

### Environment Variables

For production deployment, you might want to set:

```bash
# For Heroku/Railway
PORT=8501
```

### Custom Domain (Optional)

1. **Buy a domain** (e.g., from Namecheap, GoDaddy)
2. **Configure DNS** to point to your deployment
3. **Add custom domain** in your platform settings

## 📊 Monitoring

### Streamlit Cloud
- Built-in analytics
- Automatic scaling
- Error logs in dashboard

### Heroku
```bash
# View logs
heroku logs --tail

# Check app status
heroku ps
```

### Railway
- Real-time logs in dashboard
- Automatic restarts on errors

## 🐛 Troubleshooting

### Common Issues

1. **Port Issues**:
   ```bash
   # Make sure your app uses $PORT
   streamlit run src/python/streamlit_vrp_app.py --server.port $PORT
   ```

2. **Dependencies**:
   ```bash
   # Check requirements.txt is complete
   pip install -r requirements.txt
   ```

3. **Memory Issues**:
   - Reduce problem size in app
   - Optimize algorithm complexity

### Debug Commands

```bash
# Test locally
streamlit run src/python/streamlit_vrp_app.py

# Check Python version
python --version

# Verify dependencies
pip list
```

## 🚀 Performance Tips

1. **Optimize for Production**:
   - Reduce default problem sizes
   - Add caching for expensive computations
   - Use efficient data structures

2. **Scale Considerations**:
   - Streamlit Cloud: Handles scaling automatically
   - Heroku: Upgrade dyno for more resources
   - Railway: Automatic scaling based on usage

## 📈 Analytics

### Streamlit Cloud
- Page views
- User interactions
- Error rates

### Custom Analytics
```python
# Add to your app for custom tracking
import streamlit as st

# Track usage
if st.button("Solve VRP"):
    # Log usage
    st.write("Algorithm executed successfully")
```

## 🔒 Security

1. **Environment Variables**: Never commit secrets
2. **Input Validation**: Validate user inputs
3. **Rate Limiting**: Consider for high-traffic apps

## 📞 Support

- **Streamlit**: [Discord community](https://discord.gg/streamlit)
- **Heroku**: [Documentation](https://devcenter.heroku.com)
- **Railway**: [Documentation](https://docs.railway.app)

---

**Your VRP Algorithm Demo is now ready for deployment! 🎉** 