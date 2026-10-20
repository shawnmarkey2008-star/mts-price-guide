#!/usr/bin/env python3
"""Markey Tech Solutions Price Guide — Python 3 desktop calculator.
Run: python mts_price_guide.py (Windows) or python3 mts_price_guide.py (Mac).
Uses only Python's standard library and Tkinter. No pip packages or internet.
Specific-job prices increased 30% on October 12, 2026. Hourly rates, visit
minimums, diagnostic fees and the custom hourly-job minimum are unchanged.
Select ONE service or a custom combined job; do not double-charge overlapping work.
Active time includes diagnosis once, research, work, testing and documentation.
Unattended scans and transfers are not active labor. This produces a suggested
price, not permission to exceed a customer's previously approved quote.
To edit the catalog permanently, change SERVICES below. Rate overrides in the
window last only until another service or location is selected. Nothing is saved
unless you use Save summary. Run --self-test to check the pricing calculations.
"""
from decimal import Decimal, InvalidOperation, ROUND_CEILING, ROUND_HALF_UP
from datetime import datetime
from pathlib import Path
import sys

SERVICES = [{'name': 'Initial bench diagnosis',
  'category': 'Diagnostics',
  'minimum': 30,
  'rate': 75,
  'scope': 'Up to 30 minutes. Credit payment toward an approved repair. Extended diagnosis '
           'requires a separate approved quote.',
  'usual': '$30',
  'each': False,
  'diagnostic': True},
 {'name': 'Basic tune-up',
  'category': 'Software and setup',
  'minimum': '97.50',
  'rate': 75,
  'scope': 'Startup cleanup, updates, storage review, and performance checks.',
  'usual': '$97.5-162.5',
  'each': False,
  'diagnostic': False},
 {'name': 'Malware removal',
  'category': 'Software and setup',
  'minimum': '162.50',
  'rate': 75,
  'scope': 'Cleanup, browser review, security checks, and restart testing.',
  'usual': '$162.5-227.5',
  'each': False,
  'diagnostic': False},
 {'name': 'Severe malware or recovery',
  'category': 'Software and setup',
  'minimum': '227.50',
  'rate': 75,
  'scope': 'Approved extended cleanup or reinstall plan; backup separate.',
  'usual': '$227.5-325',
  'each': False,
  'diagnostic': False},
 {'name': 'Windows clean installation',
  'category': 'Software and setup',
  'minimum': '162.50',
  'rate': 75,
  'scope': 'OS, drivers, updates, and basic checks; valid license extra.',
  'usual': '$162.5-227.5',
  'each': False,
  'diagnostic': False},
 {'name': 'Windows installation with files',
  'category': 'Software and setup',
  'minimum': '227.50',
  'rate': 75,
  'scope': 'Standard reinstall plus up to 100 GB readable user files.',
  'usual': '$227.5-325',
  'each': False,
  'diagnostic': False},
 {'name': 'macOS reinstall or upgrade',
  'category': 'Software and setup',
  'minimum': '162.50',
  'rate': 75,
  'scope': 'Compatible OS and basic checks; recovery separate.',
  'usual': '$162.5-260',
  'each': False,
  'diagnostic': False},
 {'name': 'New PC or Mac setup',
  'category': 'Software and setup',
  'minimum': 130,
  'rate': 75,
  'scope': 'One user, updates, security settings, and up to three apps.',
  'usual': '$130-195',
  'each': False,
  'diagnostic': False},
 {'name': 'New computer and migration',
  'category': 'Software and setup',
  'minimum': '227.50',
  'rate': 75,
  'scope': 'Setup plus up to 100 GB of readable files; complex apps extra.',
  'usual': '$227.5-357.5',
  'each': False,
  'diagnostic': False},
 {'name': 'Boot failure or blue screens',
  'category': 'Software and setup',
  'minimum': 130,
  'rate': 75,
  'scope': 'Diagnose and repair a straightforward software boot issue.',
  'usual': '$130-260',
  'each': False,
  'diagnostic': False},
 {'name': 'Application installation or repair',
  'category': 'Software and setup',
  'minimum': 65,
  'rate': 75,
  'scope': 'One application; license and complex database work extra.',
  'usual': '$65-130',
  'each': False,
  'diagnostic': False},
 {'name': 'Email setup or repair',
  'category': 'Software and setup',
  'minimum': 65,
  'rate': 75,
  'scope': 'One mailbox on one device; bulk mail migration separate.',
  'usual': '$65-130',
  'each': False,
  'diagnostic': False},
 {'name': 'Account or login recovery',
  'category': 'Software and setup',
  'minimum': 65,
  'rate': 75,
  'scope': 'Authorized account recovery using supported methods.',
  'usual': '$65-162.5',
  'each': False,
  'diagnostic': False},
 {'name': 'Updates or driver repair',
  'category': 'Software and setup',
  'minimum': '97.50',
  'rate': 75,
  'scope': 'Resolve a specific update or driver issue and verify.',
  'usual': '$97.5-162.5',
  'each': False,
  'diagnostic': False},
 {'name': 'Backup configuration',
  'category': 'Software and setup',
  'minimum': '97.50',
  'rate': 75,
  'scope': 'One device and one backup destination; storage extra.',
  'usual': '$97.5-195',
  'each': False,
  'diagnostic': False},
 {'name': 'Desktop RAM upgrade',
  'category': 'Hardware and builds',
  'minimum': 65,
  'rate': 75,
  'scope': 'Install and test compatible memory.',
  'usual': '$65-97.5',
  'each': False,
  'diagnostic': False},
 {'name': 'Laptop RAM upgrade',
  'category': 'Hardware and builds',
  'minimum': 78,
  'rate': 75,
  'scope': 'Accessible replaceable RAM; soldered RAM excluded.',
  'usual': '$78-130',
  'each': False,
  'diagnostic': False},
 {'name': 'SSD or hard drive installation',
  'category': 'Hardware and builds',
  'minimum': '97.50',
  'rate': 75,
  'scope': 'Install and detect the drive; OS and cloning separate.',
  'usual': '$97.5-130',
  'each': False,
  'diagnostic': False},
 {'name': 'Drive installation and clone',
  'category': 'Hardware and builds',
  'minimum': 195,
  'rate': 75,
  'scope': 'Healthy readable source, installation, and boot verification.',
  'usual': '$195-292.5',
  'each': False,
  'diagnostic': False},
 {'name': 'Desktop power supply replacement',
  'category': 'Hardware and builds',
  'minimum': 130,
  'rate': 75,
  'scope': 'Replace supply, reconnect cables, and test.',
  'usual': '$130-195',
  'each': False,
  'diagnostic': False},
 {'name': 'Graphics card installation',
  'category': 'Hardware and builds',
  'minimum': 78,
  'rate': 75,
  'scope': 'Install card, drivers, and basic load test.',
  'usual': '$78-130',
  'each': False,
  'diagnostic': False},
 {'name': 'CPU or cooler installation',
  'category': 'Hardware and builds',
  'minimum': 130,
  'rate': 75,
  'scope': 'Compatible CPU or cooler, thermal paste, and load test.',
  'usual': '$130-195',
  'each': False,
  'diagnostic': False},
 {'name': 'Desktop motherboard replacement',
  'category': 'Hardware and builds',
  'minimum': '227.50',
  'rate': 75,
  'scope': 'Rebuild and test; OS/license remediation may add labor.',
  'usual': '$227.5-325',
  'each': False,
  'diagnostic': False},
 {'name': 'Laptop battery replacement',
  'category': 'Hardware and builds',
  'minimum': '97.50',
  'rate': 75,
  'scope': 'Compatible serviceable battery and charging check.',
  'usual': '$97.5-162.5',
  'each': False,
  'diagnostic': False},
 {'name': 'Laptop screen replacement',
  'category': 'Hardware and builds',
  'minimum': 130,
  'rate': 75,
  'scope': 'Straightforward panel replacement; bonded assemblies quoted.',
  'usual': '$130-227.5',
  'each': False,
  'diagnostic': False},
 {'name': 'Laptop keyboard or top case',
  'category': 'Hardware and builds',
  'minimum': '162.50',
  'rate': 75,
  'scope': 'Model-specific disassembly and replacement.',
  'usual': '$162.5-292.5',
  'each': False,
  'diagnostic': False},
 {'name': 'Replaceable charging port repair',
  'category': 'Hardware and builds',
  'minimum': 130,
  'rate': 75,
  'scope': 'Modular port or DC-in board; microsoldering excluded.',
  'usual': '$130-227.5',
  'each': False,
  'diagnostic': False},
 {'name': 'Desktop internal cleaning',
  'category': 'Hardware and builds',
  'minimum': 78,
  'rate': 75,
  'scope': 'Dust removal, fan checks, and inspection.',
  'usual': '$78-130',
  'each': False,
  'diagnostic': False},
 {'name': 'Laptop cleaning and repaste',
  'category': 'Hardware and builds',
  'minimum': 130,
  'rate': 75,
  'scope': 'Disassembly, cleaning, thermal paste, and temperature checks.',
  'usual': '$130-195',
  'each': False,
  'diagnostic': False},
 {'name': 'Standard custom PC build',
  'category': 'Hardware and builds',
  'minimum': 260,
  'rate': 75,
  'scope': 'Assembly, cable routing, BIOS setup, drivers, and load tests.',
  'usual': '$260-390',
  'each': False,
  'diagnostic': False},
 {'name': 'Complex build or case transfer',
  'category': 'Hardware and builds',
  'minimum': 325,
  'rate': 75,
  'scope': 'Full rebuild or difficult layout; custom water loops quoted.',
  'usual': '$325-520',
  'each': False,
  'diagnostic': False},
 {'name': 'Basic readable file transfer',
  'category': 'Files and recovery',
  'minimum': '97.50',
  'rate': 75,
  'scope': 'One healthy source, one destination, up to 100 GB.',
  'usual': '$97.5-162.5',
  'each': False,
  'diagnostic': False},
 {'name': 'Large readable transfer',
  'category': 'Files and recovery',
  'minimum': '162.50',
  'rate': 75,
  'scope': '100 GB to 1 TB; agree on folders and verification.',
  'usual': '$162.5-260',
  'each': False,
  'diagnostic': False},
 {'name': 'Very large or complex migration',
  'category': 'Files and recovery',
  'minimum': '227.50',
  'rate': 75,
  'scope': 'Over 1 TB, many sources, or complicated permissions.',
  'usual': '$227.5-390',
  'each': False,
  'diagnostic': False},
 {'name': 'Drive removal and file extraction',
  'category': 'Files and recovery',
  'minimum': 130,
  'rate': 75,
  'scope': 'Remove drive from nonworking PC/Mac; source must read normally.',
  'usual': '$130-227.5',
  'each': False,
  'diagnostic': False},
 {'name': 'Deleted file or logical recovery',
  'category': 'Files and recovery',
  'minimum': '227.50',
  'rate': 125,
  'scope': 'Healthy media; recovery tooling and verified recovered files.',
  'usual': '$227.5-455',
  'each': False,
  'diagnostic': False},
 {'name': 'Corrupt filesystem or partition',
  'category': 'Files and recovery',
  'minimum': 260,
  'rate': 125,
  'scope': 'Logical imaging and recovery without opening the drive.',
  'usual': '$260-520',
  'each': False,
  'diagnostic': False},
 {'name': 'Unstable but detectable drive',
  'category': 'Files and recovery',
  'minimum': 390,
  'rate': 125,
  'scope': 'Only suitable imaging work within capability and agreed scope.',
  'usual': '$390-780',
  'each': False,
  'diagnostic': False},
 {'name': 'Encrypted drive access',
  'category': 'Files and recovery',
  'minimum': 130,
  'rate': 75,
  'scope': 'Customer supplies valid password or recovery key; readable media.',
  'usual': '$130-227.5',
  'each': False,
  'diagnostic': False},
 {'name': 'External enclosure setup',
  'category': 'Files and recovery',
  'minimum': 65,
  'rate': 75,
  'scope': 'Fit a compatible drive and confirm access; enclosure extra.',
  'usual': '$65-97.5',
  'each': False,
  'diagnostic': False},
 {'name': 'Storage pool or NAS setup',
  'category': 'Files and recovery',
  'minimum': '227.50',
  'rate': 75,
  'scope': 'One basic system; drive health, layout, and shares.',
  'usual': '$227.5-455',
  'each': False,
  'diagnostic': False},
 {'name': 'Physical drive failure referral',
  'category': 'Files and recovery',
  'minimum': 30,
  'rate': 75,
  'scope': 'Initial assessment and referral; no internal drive repair.',
  'usual': 'Lab quote',
  'each': False,
  'diagnostic': True},
 {'name': 'USB printer setup',
  'category': 'Printers and home networking',
  'minimum': 78,
  'rate': 75,
  'scope': 'One printer on one computer; print and scan test if supported.',
  'usual': '$78-117',
  'each': False,
  'diagnostic': False},
 {'name': 'Wi-Fi printer setup',
  'category': 'Printers and home networking',
  'minimum': '97.50',
  'rate': 75,
  'scope': 'One printer, network connection, and one computer.',
  'usual': '$97.5-162.5',
  'each': False,
  'diagnostic': False},
 {'name': 'Printer troubleshooting',
  'category': 'Printers and home networking',
  'minimum': '97.50',
  'rate': 75,
  'scope': 'Drivers, queue, connectivity, and a basic mechanical check.',
  'usual': '$97.5-195',
  'each': False,
  'diagnostic': False},
 {'name': 'Additional computer on printer',
  'category': 'Printers and home networking',
  'minimum': '32.50',
  'rate': 75,
  'scope': 'Add during the same job, using existing configuration.',
  'usual': '$32.5-52',
  'each': True,
  'diagnostic': False},
 {'name': 'Label or specialty printer setup',
  'category': 'Printers and home networking',
  'minimum': 130,
  'rate': 75,
  'scope': 'Driver, media size, orientation, and sample output.',
  'usual': '$130-227.5',
  'each': False,
  'diagnostic': False},
 {'name': 'Modem and router setup',
  'category': 'Printers and home networking',
  'minimum': 130,
  'rate': 75,
  'scope': 'One modem/router, secure Wi-Fi, and connection tests.',
  'usual': '$130-195',
  'each': False,
  'diagnostic': False},
 {'name': 'Wi-Fi troubleshooting',
  'category': 'Printers and home networking',
  'minimum': '162.50',
  'rate': 75,
  'scope': 'Signal/connectivity checks and a documented fix plan.',
  'usual': '$162.5-260',
  'each': False,
  'diagnostic': False},
 {'name': 'Mesh Wi-Fi setup',
  'category': 'Printers and home networking',
  'minimum': 195,
  'rate': 75,
  'scope': 'Up to three nodes; placement, configuration, and testing.',
  'usual': '$195-325',
  'each': False,
  'diagnostic': False},
 {'name': 'Access point setup',
  'category': 'Printers and home networking',
  'minimum': 130,
  'rate': 75,
  'scope': 'One AP on an existing suitable network.',
  'usual': '$130-227.5',
  'each': False,
  'diagnostic': False},
 {'name': 'Basic switch installation',
  'category': 'Printers and home networking',
  'minimum': '97.50',
  'rate': 75,
  'scope': 'Install an unmanaged switch and check connected devices.',
  'usual': '$97.5-162.5',
  'each': False,
  'diagnostic': False},
 {'name': 'Home device network connection',
  'category': 'Printers and home networking',
  'minimum': 65,
  'rate': 75,
  'scope': 'One straightforward device; onsite minimum still applies.',
  'usual': '$65-97.5',
  'each': False,
  'diagnostic': False},
 {'name': 'Network survey and recommendations',
  'category': 'Printers and home networking',
  'minimum': '162.50',
  'rate': 75,
  'scope': 'One residential property; identify coverage and bottlenecks.',
  'usual': '$162.5-260',
  'each': False,
  'diagnostic': False},
 {'name': 'Existing cable termination or test',
  'category': 'Printers and home networking',
  'minimum': '45.50',
  'rate': 75,
  'scope': 'Accessible existing run; visit minimum applies.',
  'usual': '$45.5-78 each',
  'each': True,
  'diagnostic': False},
 {'name': 'New Ethernet cable run',
  'category': 'Printers and home networking',
  'minimum': '162.50',
  'rate': 75,
  'scope': 'Short accessible run and two terminations; cable/materials extra.',
  'usual': '$162.5-325 each',
  'each': True,
  'diagnostic': False},
 {'name': 'TV or streaming device setup',
  'category': 'Smart devices and cameras',
  'minimum': 78,
  'rate': 75,
  'scope': 'One TV/Roku/streamer, network, and customer app sign-ins.',
  'usual': '$78-130',
  'each': False,
  'diagnostic': False},
 {'name': 'Console setup or troubleshooting',
  'category': 'Smart devices and cameras',
  'minimum': '97.50',
  'rate': 75,
  'scope': 'Network, updates, storage, and basic troubleshooting.',
  'usual': '$97.5-162.5',
  'each': False,
  'diagnostic': False},
 {'name': 'Simple smart plug or bulb setup',
  'category': 'Smart devices and cameras',
  'minimum': 65,
  'rate': 75,
  'scope': 'One device; additional devices $19.5 to $32.5 during same visit.',
  'usual': '$65-97.5',
  'each': False,
  'diagnostic': False},
 {'name': 'Smart home hub setup',
  'category': 'Smart devices and cameras',
  'minimum': '162.50',
  'rate': 75,
  'scope': 'One hub and up to three compatible devices.',
  'usual': '$162.5-260',
  'each': False,
  'diagnostic': False},
 {'name': 'Home Assistant setup',
  'category': 'Smart devices and cameras',
  'minimum': 260,
  'rate': 125,
  'scope': 'Basic installation and up to five supported integrations.',
  'usual': '$260-455',
  'each': False,
  'diagnostic': False},
 {'name': 'Home automation development',
  'category': 'Smart devices and cameras',
  'minimum': '162.50',
  'rate': 125,
  'scope': 'Define triggers/actions and test; larger projects hourly.',
  'usual': '$162.5-325',
  'each': False,
  'diagnostic': False},
 {'name': 'Jellyfin or media server setup',
  'category': 'Smart devices and cameras',
  'minimum': '227.50',
  'rate': 125,
  'scope': 'One server, libraries, and one client; media supplied by customer.',
  'usual': '$227.5-390',
  'each': False,
  'diagnostic': False},
 {'name': 'Personal server remote access',
  'category': 'Smart devices and cameras',
  'minimum': 195,
  'rate': 125,
  'scope': 'Supported secure access method and verification.',
  'usual': '$195-325',
  'each': False,
  'diagnostic': False},
 {'name': 'Wi-Fi camera app setup',
  'category': 'Smart devices and cameras',
  'minimum': '97.50',
  'rate': 75,
  'scope': 'One accessible camera, network, app, and recording test.',
  'usual': '$97.5-162.5',
  'each': False,
  'diagnostic': False},
 {'name': 'Additional camera configuration',
  'category': 'Smart devices and cameras',
  'minimum': '45.50',
  'rate': 75,
  'scope': 'Same system and visit; mounting separate.',
  'usual': '$45.5-78 each',
  'each': True,
  'diagnostic': False},
 {'name': 'NVR or DVR configuration',
  'category': 'Smart devices and cameras',
  'minimum': 195,
  'rate': 75,
  'scope': 'One recorder, storage settings, and up to four existing cameras.',
  'usual': '$195-325',
  'each': False,
  'diagnostic': False},
 {'name': 'Camera mounting on accessible surface',
  'category': 'Smart devices and cameras',
  'minimum': '97.50',
  'rate': 75,
  'scope': 'Labor only; no extensive wiring or electrical work.',
  'usual': '$97.5-162.5 each',
  'each': True,
  'diagnostic': False},
 {'name': 'Four camera system configuration',
  'category': 'Smart devices and cameras',
  'minimum': 325,
  'rate': 75,
  'scope': 'Existing installed cameras; recording and client access.',
  'usual': '$325-520',
  'each': False,
  'diagnostic': False},
 {'name': 'Camera troubleshooting visit',
  'category': 'Smart devices and cameras',
  'minimum': '123.50',
  'rate': 75,
  'scope': 'Residential onsite rate; define system and fault.',
  'usual': '$123.5-247',
  'each': False,
  'diagnostic': False},
 {'name': 'Business computer setup',
  'category': 'Business and servers',
  'minimum': 195,
  'rate': 110,
  'scope': 'One workstation, updates, account, and standard apps.',
  'usual': '$195-292.5',
  'each': False,
  'diagnostic': False},
 {'name': 'Join PC to existing domain',
  'category': 'Business and servers',
  'minimum': 130,
  'rate': 110,
  'scope': 'Healthy domain, DNS, and credentials; business visit minimum.',
  'usual': '$130-195 each',
  'each': True,
  'diagnostic': False},
 {'name': 'Domain join troubleshooting',
  'category': 'Business and servers',
  'minimum': 195,
  'rate': 110,
  'scope': 'Resolve workstation/DNS issues; broader server faults hourly.',
  'usual': '$195-390',
  'each': False,
  'diagnostic': False},
 {'name': 'Microsoft 365 user setup',
  'category': 'Business and servers',
  'minimum': '97.50',
  'rate': 110,
  'scope': 'One user, mailbox/client setup, and MFA.',
  'usual': '$97.5-162.5 each',
  'each': True,
  'diagnostic': False},
 {'name': 'Microsoft 365 small tenant setup',
  'category': 'Business and servers',
  'minimum': 325,
  'rate': 110,
  'scope': 'Up to five users; licensing and bulk migration extra.',
  'usual': '$325-650',
  'each': False,
  'diagnostic': False},
 {'name': 'Mailbox migration',
  'category': 'Business and servers',
  'minimum': '162.50',
  'rate': 110,
  'scope': 'One accessible mailbox; size and source agreed.',
  'usual': '$162.5-325 each',
  'each': True,
  'diagnostic': False},
 {'name': 'QuickBooks workstation setup',
  'category': 'Business and servers',
  'minimum': '162.50',
  'rate': 110,
  'scope': 'Install/connect licensed software; bookkeeping excluded.',
  'usual': '$162.5-292.5',
  'each': False,
  'diagnostic': False},
 {'name': 'QuickBooks multiuser connectivity',
  'category': 'Business and servers',
  'minimum': '227.50',
  'rate': 110,
  'scope': 'Host/workstation troubleshooting; accounting repairs excluded.',
  'usual': '$227.5-455',
  'each': False,
  'diagnostic': False},
 {'name': 'NAS or shared folder setup',
  'category': 'Business and servers',
  'minimum': 260,
  'rate': 125,
  'scope': 'One device, defined users/groups, and access testing.',
  'usual': '$260-520',
  'each': False,
  'diagnostic': False},
 {'name': 'Business backup configuration',
  'category': 'Business and servers',
  'minimum': 260,
  'rate': 125,
  'scope': 'Defined sources, destination, schedule, and restore test.',
  'usual': '$260-520',
  'each': False,
  'diagnostic': False},
 {'name': 'Managed switch and VLAN setup',
  'category': 'Business and servers',
  'minimum': 260,
  'rate': 125,
  'scope': 'One switch, up to four VLANs, documented ports and tests.',
  'usual': '$260-520',
  'each': False,
  'diagnostic': False},
 {'name': 'Business router or firewall setup',
  'category': 'Business and servers',
  'minimum': 325,
  'rate': 125,
  'scope': 'One appliance, core routing/security, and verification.',
  'usual': '$325-650',
  'each': False,
  'diagnostic': False},
 {'name': 'VPN configuration',
  'category': 'Business and servers',
  'minimum': 260,
  'rate': 125,
  'scope': 'One gateway and one client; additional clients quoted.',
  'usual': '$260-455',
  'each': False,
  'diagnostic': False},
 {'name': 'Windows Server or Proxmox setup',
  'category': 'Business and servers',
  'minimum': 325,
  'rate': 125,
  'scope': 'Defined single-server deployment; licenses and migrations extra.',
  'usual': '$325-812.5',
  'each': False,
  'diagnostic': False},
 {'name': 'Active Directory and DNS deployment',
  'category': 'Business and servers',
  'minimum': '487.50',
  'rate': 125,
  'scope': 'One basic domain/server; workstations and migration separate.',
  'usual': '$487.5-975',
  'each': False,
  'diagnostic': False},
 {'name': 'Network documentation',
  'category': 'Business and servers',
  'minimum': 195,
  'rate': 125,
  'scope': 'Defined inventory, addressing, and connectivity diagram.',
  'usual': '$195-455',
  'each': False,
  'diagnostic': False}]
SERVICES.append(dict(name="Custom combined job", category="Custom", minimum=50,
                     rate=75, scope="Define the combined scope; count shared diagnosis and labor once.",
                     usual="Based on time", each=False, diagnostic=False))

D = Decimal
CENT = D("0.01")
def money(value):
    return D(value).quantize(CENT, rounding=ROUND_HALF_UP)

def number(value, label):
    try:
        result = D(str(value).strip())
    except (InvalidOperation, ValueError):
        raise ValueError(f"{label}: enter a number such as 0, 30 or 75.50.") from None
    if not result.is_finite() or result < 0 or result > D("10000000"):
        raise ValueError(f"{label}: enter a finite number from 0 to 10,000,000.")
    return result

def defaults(service, location):
    base = D(service["rate"])
    if service["diagnostic"]:
        return D(75), D(30)
    rate = max(base, D(95)) if location == "On-site" else base
    if location == "On-site" or base == 125:
        floor = rate
    elif location == "Remote":
        floor = rate / 2
    else:
        floor = D(50)
    return rate, floor

def calculate(service, location, values, priority="Normal"):
    v = {k: number(value, k.replace("_", " ").title()) for k, value in values.items()}
    hours, minutes, units = v["hours"], v["minutes"], v["units"]
    if hours != int(hours) or minutes != int(minutes) or minutes >= 60:
        raise ValueError("Use whole hours and whole minutes, with minutes between 0 and 59.")
    if units != int(units) or units < 1:
        raise ValueError("Units must be a whole number of at least 1.")
    if not service["each"] and units != 1:
        raise ValueError("This service is priced per job. Leave units at 1.")
    if v["rate"] <= 0:
        raise ValueError("Hourly rate must be greater than zero.")
    active = hours * 60 + minutes
    rounded = (active / 15).to_integral_value(rounding=ROUND_CEILING) * 15
    if service["diagnostic"]:
        if location != "Bench / drop-off":
            raise ValueError("The $30 assessment is bench-only. Use a custom job for a visit.")
        if active > 30:
            raise ValueError("The $30 assessment covers up to 30 minutes. Quote approved extended diagnosis as a custom job.")
        labor = D(30)
        time_charge = D(0)
    else:
        time_charge = rounded / 60 * v["rate"]
        labor = max(v["minimum"] * units, v["visit_minimum"], time_charge)
    multipliers = {"Normal": D(1), "Expedited +25%": D("1.25"), "After-hours +50%": D("1.50")}
    premium = money(labor * (multipliers[priority] - 1))
    labor = money(labor)
    parts = money(v["parts_cost"] * (1 + v["markup"] / 100))
    subtotal = labor + premium + parts + money(v["supplies"]) + money(v["travel"])
    discount = money(v["discount"])
    if discount > subtotal:
        raise ValueError("Discount cannot exceed the subtotal.")
    total = money(subtotal - discount + money(v["tax_amount"]))
    paid = money(v["paid"])
    return dict(active=active, rounded=rounded, time_charge=money(time_charge),
                labor=labor, premium=premium, parts=parts, subtotal=subtotal,
                total=total, paid=paid, balance=money(total-paid))


def self_test():
    def vals(**overrides):
        v=dict(hours="0",minutes="0",units="1",rate="75",minimum="0",visit_minimum="50",
               parts_cost="0",markup="15",supplies="0",travel="0",discount="0",tax_amount="0",paid="0")
        v.update(overrides)
        return v
    lookup={s["name"]:s for s in SERVICES}
    s=lookup["Drive installation and clone"]
    r=calculate(s,"Bench / drop-off",vals(hours="1",minutes="45",minimum=str(s["minimum"]),parts_cost="80",paid="30"))
    assert r["total"] == D("287.00") and r["balance"] == D("257.00")
    s=lookup["Wi-Fi printer setup"]
    assert calculate(s,"On-site",vals(minutes="40",rate="95",minimum=str(s["minimum"]),visit_minimum="95"))["total"] == D("97.50")
    r=calculate(s,"On-site",vals(hours="1",minutes="40",rate="95",minimum=str(s["minimum"]),visit_minimum="95"))
    assert r["rounded"] == 105 and r["total"] == D("166.25")
    s=lookup["Deleted file or logical recovery"]
    assert calculate(s,"Bench / drop-off",vals(hours="3",rate="125",minimum=str(s["minimum"]),visit_minimum="125"),"Expedited +25%")["total"] == D("468.75")
    s=lookup["Additional computer on printer"]
    assert calculate(s,"Bench / drop-off",vals(minutes="30",units="3",minimum=str(s["minimum"])))["labor"] == D("97.50")
    s=lookup["Basic tune-up"]
    assert calculate(s,"Bench / drop-off",vals(minutes="15",minimum=str(s["minimum"]),paid="100"))["balance"] == D("-2.50")
    for bad in ("-1", "NaN", "Infinity", "abc"):
        try: calculate(s,"Bench / drop-off",vals(hours=bad))
        except ValueError: pass
        else: raise AssertionError("Invalid number accepted")
    try: calculate(SERVICES[0],"Bench / drop-off",vals(minutes="31"))
    except ValueError: pass
    else: raise AssertionError("Diagnostic cap not enforced")
    assert len(SERVICES) == 87, len(SERVICES)
    print("Pricing checks passed: rounding, minimums, parts, deposits, priority, units and invalid inputs.")


def main():
    try:
        import tkinter as tk
        from tkinter import ttk, messagebox, filedialog
    except ImportError:
        print("Tkinter is missing. Install Python with Tcl/Tk support, then run this script again.")
        return
    root=tk.Tk()
    root.title("Markey Tech Solutions | Price Guide")
    root.geometry("1180x820")
    root.minsize(940,700)
    style=ttk.Style(root)
    if "clam" in style.theme_names(): style.theme_use("clam")
    style.configure("TButton",padding=7)
    style.configure("Title.TLabel",font=("Arial",20,"bold"))
    style.configure("TLabel",font=("Arial",10))
    outer=ttk.Frame(root,padding=16); outer.pack(fill="both",expand=True)
    ttk.Label(outer,text="Markey Tech Solutions",style="Title.TLabel").pack(anchor="w")
    ttk.Label(outer,text="PRICE GUIDE  •  Select a service, enter active time, calculate your suggested charge.").pack(anchor="w",pady=(3,12))
    body=ttk.Frame(outer); body.pack(fill="both",expand=True)
    left=ttk.Frame(body,width=305); left.pack(side="left",fill="y",padx=(0,16)); left.pack_propagate(False)
    ttk.Label(left,text="Find a service").pack(anchor="w")
    search=tk.StringVar(); ttk.Entry(left,textvariable=search).pack(fill="x",pady=(5,8))
    category=tk.StringVar(value="All categories")
    cats=["All categories"]+sorted({s["category"] for s in SERVICES})
    ttk.Combobox(left,textvariable=category,values=cats,state="readonly").pack(fill="x",pady=(0,8))
    listframe=ttk.Frame(left); listframe.pack(fill="both",expand=True)
    box=tk.Listbox(listframe,exportselection=False,font=("Arial",10),activestyle="none")
    scroll=ttk.Scrollbar(listframe,command=box.yview); box.configure(yscrollcommand=scroll.set)
    box.pack(side="left",fill="both",expand=True); scroll.pack(side="right",fill="y")
    ttk.Label(left,text="One service per calculation.\nUse Custom combined job for overlapping tasks.",wraplength=295).pack(anchor="w",pady=10)
    right=ttk.Frame(body); right.pack(side="left",fill="both",expand=True)
    selected=tk.StringVar(); ttk.Label(right,textvariable=selected,font=("Arial",13,"bold"),wraplength=700).pack(anchor="w")
    scope=tk.StringVar(); ttk.Label(right,textvariable=scope,wraplength=710).pack(anchor="w",pady=(4,8))
    variables={}
    form=ttk.Frame(right); form.pack(fill="x")
    form.columnconfigure(1,weight=1);form.columnconfigure(3,weight=1)
    def field(label,key,value,row,col):
        ttk.Label(form,text=label).grid(row=row,column=col,sticky="w",padx=(0,6),pady=4)
        var=tk.StringVar(value=value); variables[key]=var
        ttk.Entry(form,textvariable=var,width=12).grid(row=row,column=col+1,sticky="ew",padx=(0,14),pady=4)
    client=tk.StringVar()
    ttk.Label(form,text="Client / reference").grid(row=0,column=0,sticky="w")
    ttk.Entry(form,textvariable=client).grid(row=0,column=1,columnspan=3,sticky="ew",padx=(0,14),pady=4)
    location=tk.StringVar(value="Bench / drop-off")
    ttk.Label(form,text="Work location").grid(row=1,column=0,sticky="w")
    ttk.Combobox(form,textvariable=location,values=["Bench / drop-off","Remote","On-site"],state="readonly",width=17).grid(row=1,column=1,sticky="ew",padx=(0,14))
    priority=tk.StringVar(value="Normal")
    ttk.Label(form,text="Agreed priority").grid(row=1,column=2,sticky="w")
    ttk.Combobox(form,textvariable=priority,values=["Normal","Expedited +25%","After-hours +50%"],state="readonly",width=18).grid(row=1,column=3,sticky="ew",padx=(0,14))
    fields=[("Active hours","hours","0","Minutes (0–59)","minutes","0"),
            ("Hourly rate $","rate","75","Service minimum $","minimum","75"),
            ("Visit minimum $","visit_minimum","50","Units (per-item jobs)","units","1"),
            ("Parts cost $","parts_cost","0","Parts markup %","markup","15"),
            ("Supplies charge $","supplies","0","Agreed travel $","travel","0"),
            ("Discount $","discount","0","Tax amount $","tax_amount","0"),
            ("Already paid $","paid","0","",None,"")]
    for row,f in enumerate(fields,2):
        field(f[0],f[1],f[2],row,0)
        if f[4]: field(f[3],f[4],f[5],row,2)
    ttk.Label(right,text="Already paid includes the $30 diagnostic payment and any other deposits.\nTax is a dollar amount you determine; no automatic tax treatment is assumed.",wraplength=710).pack(anchor="w",pady=(5,8))
    actions=ttk.Frame(right);actions.pack(fill="x",pady=(0,8))
    result=tk.Text(right,height=12,wrap="word",font=("Consolas",10),padx=10,pady=10,state="disabled")
    result.pack(fill="both",expand=True)
    status=tk.StringVar(value="Prices exclude unentered parts, licenses and other costs.")
    ttk.Label(right,textvariable=status,wraplength=710).pack(anchor="w",pady=(7,0))
    visible=[]; current=[None]
    def clear_result(*_):
        result.configure(state="normal");result.delete("1.0","end");result.configure(state="disabled")
        status.set("Inputs changed. Click Calculate to refresh the suggested price.")
    def reset_rates(*_):
        s=current[0]
        if not s:return
        rate,floor=defaults(s,location.get())
        variables["rate"].set(str(rate));variables["visit_minimum"].set(str(floor))
        variables["minimum"].set(str(s["minimum"]));variables["units"].set("1")
    def choose(_=None):
        if not box.curselection():return
        s=visible[box.curselection()[0]];current[0]=s
        selected.set(s["name"])
        scope.set(s["scope"]+" Typical guide labor: "+s["usual"]+". "+("Time is TOTAL across all units." if s["each"] else "One job; units must be 1."))
        reset_rates()
    def filter_list(*_):
        query=search.get().lower().strip()
        aliases={"malware cleanup":"malware", "ssd replacement":"drive", "sd replacement":"drive", "residential printer":"printer", "pc mac":"new pc"}
        query=aliases.get(query,query)
        old=current[0];visible.clear();box.delete(0,"end")
        for s in SERVICES:
            if category.get() not in ("All categories",s["category"]):continue
            if query and query not in (s["name"]+" "+s["scope"]).lower():continue
            visible.append(s);box.insert("end",s["name"])
        if visible:
            index=visible.index(old) if old in visible else 0
            box.selection_set(index);box.see(index);choose()
        else:
            current[0]=None;selected.set("No matching services");scope.set("Try a shorter search or another category.");clear_result()
    def summary():
        if current[0] is None:raise ValueError("Select a service first.")
        s=current[0];v={k:x.get() for k,x in variables.items()}
        r=calculate(s,location.get(),v,priority.get())
        balance_label="Credit / overpayment" if r["balance"]<0 else "BALANCE DUE"
        return (f"MARKEY TECH SOLUTIONS — SUGGESTED PRICE\n"
                f"{datetime.now():%Y-%m-%d %H:%M} | {client.get().strip() or 'No client entered'}\n"
                f"Service: {s['name']} | {location.get()} | Units: {v['units']}\n"
                f"Scope: {s['scope']}\n"
                f"Active time: {r['active']} min | Rounded: {r['rounded']} min\n"
                f"Hourly rate: ${D(v['rate']):,.2f} | Service minimum/unit: ${D(v['minimum']):,.2f}\n"
                f"Visit minimum: ${D(v['visit_minimum']):,.2f}\n"
                f"Labor (minimum or time): ${r['labor']:,.2f}\n"
                f"Priority ({priority.get()}): ${r['premium']:,.2f}\n"
                f"Parts including {v['markup']}% markup: ${r['parts']:,.2f}\n"
                f"Supplies: ${money(v['supplies']):,.2f} | Travel: ${money(v['travel']):,.2f}\n"
                f"Discount: -${money(v['discount']):,.2f} | Tax entered: ${money(v['tax_amount']):,.2f}\n"
                f"JOB TOTAL: ${r['total']:,.2f}\n"
                f"Already paid: -${r['paid']:,.2f}\n"
                f"{balance_label}: ${abs(r['balance']):,.2f}\n\n"
                "Suggested price only. Confirm scope and customer approval before billing.\n"
                "Count active labor only. Do not stack overlapping service charges.\n")
    def run(action="calculate"):
        try:
            text=summary()
            result.configure(state="normal");result.delete("1.0","end");result.insert("1.0",text);result.configure(state="disabled")
            status.set("Calculated. Review the scope and agreed price before billing.")
            if action=="copy":
                root.clipboard_clear();root.clipboard_append(text);status.set("Summary copied.")
            elif action=="save":
                path=filedialog.asksaveasfilename(defaultextension=".txt",initialfile="MTS_Quote_"+datetime.now().strftime("%Y%m%d_%H%M%S")+".txt",filetypes=[("Text file","*.txt")])
                if path:Path(path).write_text(text,encoding="utf-8");status.set("Summary saved.")
        except (ValueError,OSError,InvalidOperation) as exc:
            clear_result();messagebox.showerror("Check your entries",str(exc))
    ttk.Button(actions,text="Calculate price",command=run).pack(side="left")
    ttk.Button(actions,text="Copy summary",command=lambda:run("copy")).pack(side="left",padx=8)
    ttk.Button(actions,text="Save summary",command=lambda:run("save")).pack(side="left")
    ttk.Button(actions,text="Reset service rates",command=reset_rates).pack(side="right")
    for var in list(variables.values())+[client,priority]:var.trace_add("write",clear_result)
    search.trace_add("write",filter_list);category.trace_add("write",filter_list)
    location.trace_add("write",reset_rates);box.bind("<<ListboxSelect>>",choose)
    root.bind("<Return>",lambda _:run())
    filter_list()
    root.mainloop()

if __name__ == "__main__":
    if "--self-test" in sys.argv:self_test()
    else:main()
