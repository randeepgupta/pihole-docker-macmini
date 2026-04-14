# Home-Lab: Network-Wide Ad-Blocking with Pi-hole & Docker

## 🌐 Overview
A technical implementation of a network-level DNS sinkhole deployed on a **Mac Mini** (host) within an **eero Mesh Wi-Fi** environment. This project aims to improve network performance, privacy, and user experience for all connected devices by filtering advertisements and telemetry at the source.

## 🏗️ Architecture
* **Host Hardware:** Mac Mini 
* **Virtualization:** Docker Desktop for macOS
* **Container:** Pi-hole (Official Image)
* **Network Infrastructure:** eero 6 Mesh System
* **Primary DNS:** Local Pi-hole Instance (`192.168.5.73`)
* **Secondary DNS (Safety Net):** Cloudflare (`1.1.1.1`)

## 🛠️ Implementation Details

### 1. Persistent Storage
To ensure settings survive container updates, local directories were mapped to the container:
* `~/pihole/etc-pihole` ➔ `/etc/pihole`
* `~/pihole/etc-dnsmasq.d` ➔ `/etc/dnsmasq.d`

### 2. High Availability (The "Safety Net")
To prevent network downtime in the event of host failure, a **Secondary DNS** was configured at the router level. 
* **Design Choice:** While a secondary DNS may allow some ads to pass through if the primary fails to respond in time, it ensures 100% uptime for a multi-user household—balancing ad-filtering with service reliability.

### 3. Deployment
The container was deployed via Docker CLI (or Docker Compose) with the following parameters:
```bash
docker run -d \
  --name pihole \
  -p 53:53/tcp -p 53:53/udp \
  -p 80:80 \
  -e TZ="America/Chicago" \
  -e WEBPASSWORD="<REDACTED>" \
  -v "$(pwd)/etc-pihole:/etc/pihole" \
  -v "$(pwd)/etc-dnsmasq.d:/etc/dnsmasq.d" \
  --restart=unless-stopped \
  pihole/pihole:latest
```

## 📈 Key Results
* **Privacy:** Blocked trackers from Smart TVs and IoT devices.
* **Performance:** Reduced bandwidth consumption by preventing ad-media loads.
* **Accessibility:** Centralized management via a web-based dashboard.

## 💡 Lessons Learned
* **IP Allocation:** Importance of DHCP reservations in mesh networks (eero) to prevent DNS "black holes."
* **MacOS Constraints:** Managing sleep/power settings on a headless Mac Mini to ensure 24/7 service availability.
