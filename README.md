# MiniPOS-Cloud ☁️
A simplified, cloud-based Point-of-Sale backend built using Django and the Django REST Framework (DRF).
This project simulates how multiple store branches could manage sales, customers, and inventory — designed to be scalable, resilient, and ready for cloud deployment.

## 🚀 Features
CRUD APIs for:

- Products

- Customers

- Orders

- Payments

- Automatic subtotal and total calculations for orders

- Basic sales analytics endpoints (coming soon)

## 🔜 Advanced / Planned Features

- Offline Mode Simulation — store data locally and sync when online

- Celery & Redis Integration — for background jobs (e.g., syncing sales or sending receipts)

- Rate limiting + retry logic for failed API calls

- Health check endpoints for monitoring

- Dockerized setup for production deployment with Redis + PostgreSQL

- Hosting

## 🥞Tech-Stack
### Backend: Django + Django REST framework
### Database: PostgreSQL
### Task Queue (planned):	Celery + Redis
### Testing:	Pytest + Django test client
### Containerization (planned):	Docker + Docker Compose
### Caching (planned):	Redis

## ⚙️Get started 
```bash
git clone git@github.com:bbell2411/MiniPOS-Cloud.git
cd MiniPOS-Cloud
```

### Virtual Env
```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate  # Windows
```
### Install Dependancies
```bash
make install
```
### Run Migrations
```bash
make migrations
```
### Seed Database
```bash
make seed
```
### Test
```bash
make test
```
### Run Server
```bash
make run
```
## 💡 Next Steps

- Add authentication (JWT or session-based)

- Build analytics endpoints for revenue & top-selling products

- Add Celery & Redis for async tasks

- Dockerize the project


