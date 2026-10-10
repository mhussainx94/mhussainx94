<div align="center">

<table>
<tr>
<td width="420" align="center" valign="middle">

<img src="assets/identity-particle.gif" width="360" alt="Particle animation: the Kali Linux dragon dissolves into a cloud of particles that reforms as a particle portrait of Muhammad Hussain, then returns to the logo" />

</td>
<td valign="middle" align="left">

# Hi, I'm Muhammad Hussain

**Cybersecurity-focused Computer Science student** working toward penetration testing and application security through a hands-on lab, security tooling, vulnerability assessment and documented practice.

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white) ![Linux](https://img.shields.io/badge/Linux-FCC624?style=flat&logo=linux&logoColor=black) ![Kali Linux](https://img.shields.io/badge/Kali_Linux-557C94?style=flat&logo=kalilinux&logoColor=white) ![Burp Suite](https://img.shields.io/badge/Burp_Suite-FF6633?style=flat&logo=burpsuite&logoColor=white) ![OWASP](https://img.shields.io/badge/OWASP-000000?style=flat&logo=owasp&logoColor=white) ![Nmap](https://img.shields.io/badge/Nmap-4A90D9?style=flat&logo=nmap&logoColor=white) ![Git](https://img.shields.io/badge/Git-F05032?style=flat&logo=git&logoColor=white) ![VS Code](https://img.shields.io/badge/VS_Code-007ACC?style=flat&logo=visualstudiocode&logoColor=white) ![Bash](https://img.shields.io/badge/Bash-4EAA25?style=flat&logo=gnubash&logoColor=white) ![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white) ![OWASP ZAP](https://img.shields.io/badge/OWASP_ZAP-00549E?style=flat&logo=owasp&logoColor=white) ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=flat&logo=postgresql&logoColor=white) ![Wireshark](https://img.shields.io/badge/Wireshark-1679A7?style=flat&logo=wireshark&logoColor=white) ![Metasploit](https://img.shields.io/badge/Metasploit-2596CD?style=flat&logo=metasploit&logoColor=white) ![TryHackMe](https://img.shields.io/badge/TryHackMe-212C42?style=flat&logo=tryhackme&logoColor=white) ![Hack The Box](https://img.shields.io/badge/Hack_The_Box-9FEF00?style=flat&logo=hackthebox&logoColor=black) ![OpenVAS](https://img.shields.io/badge/OpenVAS-008B5A?style=flat&logoColor=white) ![Network Security](https://img.shields.io/badge/Network_Security-2B579A?style=flat&logoColor=white) ![Security Automation](https://img.shields.io/badge/Security_Automation-5A32A3?style=flat&logoColor=white) ![Web Security](https://img.shields.io/badge/Web_Security-0B7285?style=flat&logoColor=white)

</td>
</tr>
</table>

</div>

<br>

```text
$ whoami
muhammad-hussain

$ focus
web-security
application-security
penetration-testing
vulnerability-assessment

$ environment
kali-linux
linux
burp-suite
python
security-labs

$ status
building // testing // documenting
```

---

## Security focus

Direction, not a claim of expertise. I keep these three things separate on purpose.

| | |
| --- | --- |
| **Hands-on now** | Built a Python security scanner for Odoo deployments · operate and document a multi-OS personal cyber lab (infrastructure) · TryHackMe practice · Secure SDLC and application security assessment exposure during a security internship |
| **Developing toward** | Professional penetration testing · application security · authorized security assessments · vulnerability research · bug bounty methodology |
| **Planned** | API security testing · cloud security labs · Active Directory · container / Docker security · CI/CD security · malware analysis · SOC / blue-team exercises · detection engineering |

Primary areas: Web Application Security · Vulnerability Assessment · Penetration Testing · Application Security · Secure SDLC · API Security · Security Automation · Linux Security.

---

## Projects

### Security engineering

#### [Odoo Security Scanner](https://github.com/mhussainx94/odoo-security-scanner) `v2.0`

A vulnerability-assessment tool for Odoo deployments, written in Python with a Flask interface and a CLI.

| | |
| --- | --- |
| **Problem** | A repeatable way to assess an Odoo deployment's exposure and configuration |
| **Tests** | Open ports and services · SSL/TLS · HTTP security headers · cookies · Odoo-specific endpoints · authentication · matching against a bundled CVE database |
| **Produces** | JSON, TXT and HTML reports |
| **Why it matters** | Brings network, transport, HTTP and application-level checks into one tool with machine-readable and human-readable output |

<!-- PENDING: verify every line above against odoo-security-scanner/README.md and source. Capabilities come from my brief, not from the repo. -->

#### [Personal Cybersecurity Lab](https://github.com/mhussainx94/personal-cyber-lab) `Active / Evolving`

A personally operated lab for hands-on learning in web security, network security, vulnerability assessment and penetration testing. It is a real multi-OS architecture, not a list of installed tools.

<div align="center">
<img src="assets/cyber-lab-architecture.svg" width="860" alt="Lab architecture: a physical laptop runs Windows 11 with VMware Workstation hosting Kali-NAT, Kali-Bridged, Kali-Host-Only, Metasploitable, Windows 10 with DVWA, Ubuntu and Ubuntu Server over NAT, Bridged and Host-Only networking. The same laptop triple-boots Kali Linux and Debian, and uses Tails and Kali live USB environments." />
</div>

<br>

Windows 11, Kali Linux and Debian are separate operating systems on one triple-boot machine. Tails and Kali run as independent live-boot USB environments. VMware Workstation runs under Windows 11.

**Honest status.** The infrastructure exists. Testing on it has not started.

| Area | Status |
| ---- | ------ |
| Infrastructure | `ACTIVE` |
| Architecture documentation | `ACTIVE` |
| Web security testing (DVWA) | `NOT YET TESTED` |
| Network security testing | `NOT YET TESTED` |
| Vulnerability assessment | `NOT YET TESTED` |
| Penetration testing | `NOT YET TESTED` |
| Security automation | `PLANNED` |

### Security automation and research

#### [VDP-PRO Safe Recon](https://github.com/mhussainx94/vdp-pro-safe-recon)

Authorized, passive reconnaissance and security automation in **Bash**, built around a repeatable workflow and a safe testing methodology. It is a personal workflow project, not an offensive reconnaissance platform.

<!-- PENDING: add concrete behaviour (inputs, outputs, what it does and does not touch) from vdp-pro-safe-recon/README.md and main script. -->

#### [Onion Web Crawler](https://github.com/mhussainx94/onion-web-crawler)

A research and security-tooling project in **Python** that works over **Tor**.

<!-- PENDING: one sentence on the technical purpose (what it crawls, what it records, how) from onion-web-crawler/README.md. -->

### Hands-on security learning

#### [TryHackMe](https://github.com/mhussainx94/TryHackMe)

Documented practical labs and applied learning on security concepts.

<!-- PENDING: name the rooms/paths actually completed, from the TryHackMe repo contents. -->

### Systems and technical projects

#### [CipherLog Assembly](https://github.com/mhussainx94/CipherLog-Assembly)

A lower-level, systems-oriented project written in assembly.

<!-- PENDING: describe what it does from CipherLog-Assembly/README.md (architecture, assembler, purpose). -->

#### [Portfolio](https://github.com/mhussainx94/mhussainx94-portfolio)

Personal portfolio site: [mhussainx94-portfolio.vercel.app](https://mhussainx94-portfolio.vercel.app)

---

## Experience

**Software Security Intern** · National CERT, Pakistan

<!-- PENDING: add dates and location if you want them shown. -->

- Exposure to Secure SDLC practices
- Exposure to application security assessment
- Vulnerability identification and remediation-oriented work
- Security testing methodologies and industry-standard security tools

---

## Security profile

Grouped by domain. Not rated: the evidence is in the projects above.

| Domain | Areas |
| ------ | ----- |
| **Web and application security** | Web Application Security · OWASP Top 10 · VAPT · Secure SDLC · Vulnerability Identification · Remediation |
| **Security testing** | Burp Suite · OWASP ZAP · Nmap · Vulnerability Assessment · Network Scanning · Security Testing Methodologies |
| **Programming and automation** | Python · Bash · SQL |
| **Operating systems** | Kali Linux · Linux · Windows |
| **Networking** | Computer Networking · Network Security · TCP/IP fundamentals · Network Scanning |

<!-- PENDING: Burp Suite, OWASP ZAP, Nmap and SQL come from my brief's example list. Confirm each is something you have actually used before publishing. -->

### Skills and tools

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white) ![Linux](https://img.shields.io/badge/Linux-FCC624?style=flat&logo=linux&logoColor=black) ![Kali Linux](https://img.shields.io/badge/Kali_Linux-557C94?style=flat&logo=kalilinux&logoColor=white) ![Burp Suite](https://img.shields.io/badge/Burp_Suite-FF6633?style=flat&logo=burpsuite&logoColor=white) ![OWASP](https://img.shields.io/badge/OWASP-000000?style=flat&logo=owasp&logoColor=white) ![Nmap](https://img.shields.io/badge/Nmap-4A90D9?style=flat&logo=nmap&logoColor=white) ![Git](https://img.shields.io/badge/Git-F05032?style=flat&logo=git&logoColor=white) ![VS Code](https://img.shields.io/badge/VS_Code-007ACC?style=flat&logo=visualstudiocode&logoColor=white) ![Bash](https://img.shields.io/badge/Bash-4EAA25?style=flat&logo=gnubash&logoColor=white) ![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white) ![OWASP ZAP](https://img.shields.io/badge/OWASP_ZAP-00549E?style=flat&logo=owasp&logoColor=white) ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=flat&logo=postgresql&logoColor=white) ![Wireshark](https://img.shields.io/badge/Wireshark-1679A7?style=flat&logo=wireshark&logoColor=white) ![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat&logo=github&logoColor=white) ![Windows](https://img.shields.io/badge/Windows-0078D4?style=flat&logo=windows&logoColor=white) ![Flask](https://img.shields.io/badge/Flask-000000?style=flat&logo=flask&logoColor=white) ![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat&logo=html5&logoColor=white) ![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat&logo=javascript&logoColor=black)

![C++](https://img.shields.io/badge/C++-00599C?style=flat&logo=cplusplus&logoColor=white) ![Java](https://img.shields.io/badge/Java-ED8B00?style=flat&logo=openjdk&logoColor=white) ![MIPS Assembly](https://img.shields.io/badge/MIPS_Assembly-525252?style=flat&logoColor=white) ![SQL](https://img.shields.io/badge/SQL-336791?style=flat&logo=postgresql&logoColor=white) ![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=flat&logo=githubactions&logoColor=white) ![VMware](https://img.shields.io/badge/VMware-607078?style=flat&logo=vmware&logoColor=white) ![Ubuntu](https://img.shields.io/badge/Ubuntu-E95420?style=flat&logo=ubuntu&logoColor=white) ![Debian](https://img.shields.io/badge/Debian-A81D33?style=flat&logo=debian&logoColor=white) ![Fedora](https://img.shields.io/badge/Fedora-51A2DA?style=flat&logo=fedora&logoColor=white) ![Metasploit](https://img.shields.io/badge/Metasploit-2596CD?style=flat&logo=metasploit&logoColor=white) ![OpenVAS](https://img.shields.io/badge/OpenVAS-008B5A?style=flat&logoColor=white) ![TryHackMe](https://img.shields.io/badge/TryHackMe-212C42?style=flat&logo=tryhackme&logoColor=white) ![Hack The Box](https://img.shields.io/badge/Hack_The_Box-9FEF00?style=flat&logo=hackthebox&logoColor=black) ![Cloudflare](https://img.shields.io/badge/Cloudflare-F38020?style=flat&logo=cloudflare&logoColor=white) ![AWS](https://img.shields.io/badge/AWS-232F3E?style=flat&logo=amazonwebservices&logoColor=white) ![Next.js](https://img.shields.io/badge/Next.js-000000?style=flat&logo=nextdotjs&logoColor=white) ![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=flat&logo=typescript&logoColor=white) ![n8n](https://img.shields.io/badge/n8n-EA4B71?style=flat&logo=n8n&logoColor=white) ![Postman](https://img.shields.io/badge/Postman-FF6C37?style=flat&logo=postman&logoColor=white) ![Packet Tracer](https://img.shields.io/badge/Packet_Tracer-0078D4?style=flat&logo=cisco&logoColor=white)
**Security disciplines:** Web Application Security · Penetration Testing · Vulnerability Assessment · OWASP Top 10 · Application Security · Secure SDLC · Network Security · Security Automation

### Learning path

```text
Linux → Networking → HTTP/HTTPS → Web Applications → Authentication & Authorization
      → Burp Suite → OWASP → Advanced Web Vulnerabilities → API Security → Penetration Testing
```

---

## Certifications

| Certification | Issuer | Issued |
| ------------- | ------ | ------ |
| Google Cybersecurity | Google | Dec 2025 |
| Tools of the Trade: Linux and SQL | Google | Dec 2025 |
| Cybersecurity for Everyone | University of Maryland | Aug 2025 |
| Kali Linux | Coursera / Board Infinity | Jul 2025 |
| CyberSecurity | Asian Development Bank | Jun 2025 |
| Generative AI Essentials | IBM | Aug 2025 |
| Data Analyst | OneRoadmap | May 2025 |

<!-- ISC2 Candidate is deliberately omitted: its listed validity ended July 2026. -->

<!-- PENDING: Education section. The brief was cut off at "National University of Technol...". Send the full degree, institution and dates. -->

---

## Connect

[GitHub](https://github.com/mhussainx94) · [Portfolio](https://mhussainx94-portfolio.vercel.app)

<!-- PENDING: add LinkedIn (and any other link you want) once you send the URL. -->
