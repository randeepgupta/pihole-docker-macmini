import subprocess
import socket

def check_internet():
    """Checks if the Mac Mini can reach a public server (Cloudflare)."""
    try:
        socket.create_connection(("1.1.1.1", 53), timeout=3)
        return "✅ Internet: Online"
    except OSError:
        return "❌ Internet: Offline"

def check_docker_container():
    """Checks if the 'pihole' container is currently running."""
    try:
        result = subprocess.check_output(["docker", "inspect", "-f", "{{.State.Running}}", "pihole"])
        if result.decode().strip() == "true":
            return "✅ Docker: Pi-hole container is running"
    except Exception:
        pass
    return "❌ Docker: Pi-hole container is STOPPED"

def check_dns_resolution():
    """Checks if Pi-hole is successfully resolving a domain name."""
    try:
        # We tell the 'nslookup' command to specifically use your Pi-hole (localhost)
        output = subprocess.check_output(["nslookup", "google.com", "127.0.0.1"], timeout=3)
        if b"Address:" in output:
            return "✅ DNS: Pi-hole is resolving queries"
    except Exception:
        pass
    return "❌ DNS: Pi-hole is NOT resolving (check your setup)"

if __name__ == "__main__":
    print("-" * 30)
    print("🏠 MCKINNEY HOME-LAB HEALTH CHECK")
    print("-" * 30)
    print(check_internet())
    print(check_docker_container())
    print(check_dns_resolution())
    print("-" * 30)
