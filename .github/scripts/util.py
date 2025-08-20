import re
import json
import os
from datetime import datetime
import time

# Set the TZ environment variable to PST
os.environ['TZ'] = 'America/Los_Angeles'
time.tzset()

# SIMPLIFY_BUTTON = "https://i.imgur.com/kvraaHg.png"
SIMPLIFY_BUTTON = "https://i.imgur.com/MXdpmi0.png" # says apply
SHORT_APPLY_BUTTON = "https://i.imgur.com/fbjwDvo.png"
SQUARE_SIMPLIFY_BUTTON = "https://i.imgur.com/aVnQdox.png"
LONG_APPLY_BUTTON = "https://i.imgur.com/6cFAMUo.png"
NON_SIMPLIFY_INACTIVE_THRESHOLD_MONTHS = 3
SIMPLIFY_INACTIVE_THRESHOLD_MONTHS = 6

# Set of Simplify company URLs to block from appearing in the README
# Add Simplify company URLs to block them (e.g., "https://simplify.jobs/c/Jerry")
BLOCKED_COMPANIES = {
    "https://simplify.jobs/c/Jerry",
}

# FAANG+ companies - will be marked with fire emoji
FAANG_PLUS = {
    "airbnb", "adobe", "amazon", "apple", "asana", "atlassian", "bytedance", "cloudflare","coinbase", "databricks", "datadog",
    "doordash", "dropbox", "duolingo", "figma", "google", "ibm", "instacart", "linkedin", "lyft", "meta", "microsoft",
    "netflix", "notion", "nvidia", "openai", "oracle", "palantir", "paypal", "pinterest", "ramp", "reddit","rippling", "robinhood", "roblox",
    "salesforce", "samsara", "shopify", "slack", "snap", "snapchat", "splunk","snowflake", "stripe", "square", "tesla", "tinder","tiktok", "uber",
    "visa","waymo", "x"
}

CATEGORIES = {
    "Software": {"name": "Software Engineering", "emoji": "💻"},
    "Product": {"name": "Product Management", "emoji": "📱"},
    "AI/ML/Data": {"name": "Data Science, AI & Machine Learning", "emoji": "🤖"},
    "Quant": {"name": "Quantitative Finance", "emoji": "📈"},
    "Hardware": {"name": "Hardware Engineering", "emoji": "🔧"},
    "Other": {"name": "Other", "emoji": "💼"}
}

def setOutput(key, value):
    if output := os.getenv('GITHUB_OUTPUT', None):
        with open(output, 'a') as fh:
            print(f'{key}={value}', file=fh)

def fail(why):
    setOutput("error_message", why)
    exit(1)

def getLocations(listing):
    locations = "</br>".join(listing["locations"])
    return locations

def getSponsorship(listing):
    if listing["sponsorship"] == "Does Not Offer Sponsorship":
        return " 🛂"
    elif listing["sponsorship"] == "U.S. Citizenship is Required":
        return " 🇺🇸"
    return ""

def getLink(listing):
    if not listing["active"]:
        return "🔒"
    link = listing["url"] 
    if "?" not in link:
        link += "?utm_source=Simplify&ref=Simplify"
    else:
        link += "&utm_source=Simplify&ref=Simplify"

    if listing["source"] != "Simplify":
        # Non-Simplify jobs: single button, centered with smaller width to prevent wrapping
        return (
            f'<div align="center">'
            f'<a href="{link}"><img src="{LONG_APPLY_BUTTON}" width="80" alt="Apply"></a>'
            f'</div>'
        )

    # Simplify jobs: two buttons with smaller widths to prevent wrapping
    simplifyLink = f"https://simplify.jobs/p/{listing['id']}?utm_source=GHList"
    return (
        f'<div align="center">'
        f'<a href="{link}"><img src="{SHORT_APPLY_BUTTON}" width="50" alt="Apply"></a> '
        f'<a href="{simplifyLink}"><img src="{SQUARE_SIMPLIFY_BUTTON}" width="26" alt="Simplify"></a>'
        f'</div>'
    )
    
def mark_stale_listings(listings):
    now = datetime.now()
    for listing in listings:
        age_in_months = (now - datetime.fromtimestamp(listing["date_posted"])).days / 30
        if listing["source"] != "Simplify" and age_in_months >= NON_SIMPLIFY_INACTIVE_THRESHOLD_MONTHS:
                listing["active"] = False
        elif listing["source"] == "Simplify" and age_in_months >= SIMPLIFY_INACTIVE_THRESHOLD_MONTHS:
            listing["active"] = False
    return listings

def filter_active(listings):
    return [listing for listing in listings if listing.get("active", False)]

def convert_markdown_to_html(text):
    """Convert markdown formatting to HTML for proper rendering in HTML table cells"""
    # Convert **bold** to <strong>bold</strong>
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    
    # Convert [link text](url) to <a href="url">link text</a>
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
    
    return text

def create_md_table(listings, offSeason=False):
    # Create HTML table with CSS styling
    table = '<table style="width: 100%; border-collapse: collapse;">\n<thead>\n<tr>\n'
    
    if offSeason:
        table += '<th style="width: 22%; min-width: 180px; padding: 8px; text-align: left; border-bottom: 2px solid #ddd;">Company</th>\n'
        table += '<th style="width: 22%; min-width: 180px; padding: 8px; text-align: left; border-bottom: 2px solid #ddd;">Role</th>\n'
        table += '<th style="width: 18%; min-width: 140px; padding: 8px; text-align: left; border-bottom: 2px solid #ddd;">Location</th>\n'
        table += '<th style="width: 15%; min-width: 120px; padding: 8px; text-align: left; border-bottom: 2px solid #ddd;">Terms</th>\n'
        table += '<th style="width: 15%; min-width: 120px; padding: 8px; text-align: center; border-bottom: 2px solid #ddd;">Application</th>\n'
        table += '<th style="width: 8%; min-width: 60px; padding: 8px; text-align: center; border-bottom: 2px solid #ddd;">Age</th>\n'
    else:
        table += '<th style="width: 25%; min-width: 200px; padding: 8px; text-align: left; border-bottom: 2px solid #ddd;">Company</th>\n'
        table += '<th style="width: 30%; min-width: 250px; padding: 8px; text-align: left; border-bottom: 2px solid #ddd;">Role</th>\n'
        table += '<th style="width: 20%; min-width: 150px; padding: 8px; text-align: left; border-bottom: 2px solid #ddd;">Location</th>\n'
        table += '<th style="width: 15%; min-width: 120px; padding: 8px; text-align: center; border-bottom: 2px solid #ddd;">Application</th>\n'
        table += '<th style="width: 10%; min-width: 80px; padding: 8px; text-align: center; border-bottom: 2px solid #ddd;">Age</th>\n'
    
    table += '</tr>\n</thead>\n<tbody>\n'

    prev_company = None
    prev_days_active = None  # FIXED: previously incorrectly using date_posted

    for listing in listings:
        # Add fire emoji for FAANG+ companies
        company_name = listing["company_name"]
        if company_name.lower() in FAANG_PLUS:
            company_name = f"🔥 {company_name}"
            listing["company_name"] = company_name  # Update the listing as well
        
        raw_url = listing.get("company_url", "").strip()
        company_url = raw_url + '?utm_source=GHList&utm_medium=company' if raw_url.startswith("http") else ""
        company_markdown = f"**[{company_name}]({company_url})**" if company_url else f"**{company_name}**"
        company = convert_markdown_to_html(company_markdown)
        location = getLocations(listing)
        
        # Check for advanced degree requirements and add graduation cap emoji
        title_with_degree_emoji = listing["title"]
        
        # Check degrees field for advanced degree requirements
        degrees = listing.get("degrees", [])
        if degrees:
            # Check if only advanced degrees are required (no Bachelor's or Associate's)
            has_bachelors_or_associates = any(
                degree.lower() in ["bachelor's", "associate's"]
                for degree in degrees
            )
            has_advanced_degrees = any(
                degree.lower() in ["master's", "phd", "mba"]
                for degree in degrees
            )
            
            if has_advanced_degrees and not has_bachelors_or_associates:
                title_with_degree_emoji += " 🎓"
        
        # Also check title text for degree mentions
        title_lower = listing["title"].lower()
        if any(term in title_lower for term in ["master's", "masters", "master", "mba", "phd", "ph.d", "doctorate", "doctoral"]):
            if "🎓" not in title_with_degree_emoji:
                title_with_degree_emoji += " 🎓"
        
        position = title_with_degree_emoji + getSponsorship(listing)
        terms = ", ".join(listing["terms"])
        link = getLink(listing)

        # calculate days active
        days_active = (datetime.now() - datetime.fromtimestamp(listing["date_posted"])).days
        days_active = max(days_active, 0)  # in case somehow negative
        days_display = (
            "0d" if days_active == 0 else
            f"{(days_active // 30)}mo" if days_active > 30 else
            f"{days_active}d"
        )
            
        # FIXED: comparison to see if same company and same days active
        if prev_company == company_name and prev_days_active == days_active:
            company = "↳"
        else:
            prev_company = company_name
            prev_days_active = days_active
        
        # Create HTML table row
        table += '<tr>\n'
        
        if offSeason:
            table += f'<td style="padding: 8px; border-bottom: 1px solid #eee;">{company}</td>\n'
            table += f'<td style="padding: 8px; border-bottom: 1px solid #eee;">{position}</td>\n'
            table += f'<td style="padding: 8px; border-bottom: 1px solid #eee;">{location}</td>\n'
            table += f'<td style="padding: 8px; border-bottom: 1px solid #eee;">{terms}</td>\n'
            table += f'<td style="padding: 8px; border-bottom: 1px solid #eee; text-align: center;">{link}</td>\n'
            table += f'<td style="padding: 8px; border-bottom: 1px solid #eee; text-align: center;">{days_display}</td>\n'
        else:
            table += f'<td style="padding: 8px; border-bottom: 1px solid #eee;">{company}</td>\n'
            table += f'<td style="padding: 8px; border-bottom: 1px solid #eee;">{position}</td>\n'
            table += f'<td style="padding: 8px; border-bottom: 1px solid #eee;">{location}</td>\n'
            table += f'<td style="padding: 8px; border-bottom: 1px solid #eee; text-align: center;">{link}</td>\n'
            table += f'<td style="padding: 8px; border-bottom: 1px solid #eee; text-align: center;">{days_display}</td>\n'
        
        table += '</tr>\n'

    table += '</tbody>\n</table>\n'
    return table



def getListingsFromJSON(filename=".github/scripts/listings.json"):
    with open(filename) as f:
        listings = json.load(f)
        print(f"Received {len(listings)} listings from listings.json")
        return listings


def classifyJobCategory(job):
    # First check if there's an existing category
    if "category" in job and job["category"]:
        # Map the existing category to our standardized categories
        category = job["category"].lower()
        if category in ["hardware", "hardware engineering", "embedded engineering"]:
            return "Hardware Engineering"
        elif category in ["quant", "quantitative finance", "fintech engineering", "fintech"]:
            return "Quantitative Finance"
        elif category in ["ai/ml/data", "data & analytics", "ai & machine learning", "data science"]:
            return "Data Science, AI & Machine Learning"
        elif category in ["product", "product management"]:
            return "Product Management"
        elif category in ["software", "software engineering"]:
            return "Software Engineering"
        elif category in ["other"]:
            return "Other"
    
    # If no category exists or it's not recognized, classify by title
    # Order of filtering based on title: hardware -> quant -> data science -> software eng -> product -> other
    title = job.get("title", "").lower()
    
    # Hardware (first priority)
    if any(term in title for term in ["hardware", "embedded", "fpga", "circuit", "chip", "silicon", "asic", "robotics", "firmware", "manufactur"]):
        return "Hardware Engineering"
    
    # Quant (second priority)
    elif any(term in title for term in ["quant", "quantitative", "trading", "finance", "investment"]):
        return "Quantitative Finance"
    
    # Data Science (third priority)
    elif any(term in title for term in ["data science", "artificial intelligence", "data scientist", "ai &", "machine learning", "ml", "data analytics", "data analyst", "research eng", "nlp", "computer vision", "research sci", "data eng"]):
        return "Data Science, AI & Machine Learning"
    
    # Software Engineering (fourth priority)
    elif any(term in title for term in ["forward deployed", "forward-deployed","software", "software eng", "software dev", "product engineer", "fullstack", "full-stack", "full stack", "frontend", "front end", "front-end", "backend", "back end", "back-end", "founding engineer", "mobile dev", "mobile engineer"]):
        return "Software Engineering"
    
    # Product (fifth priority)
    elif any(term in title for term in ["product manag", "product analyst", "apm"]) or ("product" in title and "analyst" in title):
        return "Product Management"
    
    # Other (everything else)
    else:
        return "Other"

def ensureCategories(listings):
    for listing in listings:
        listing["category"] = classifyJobCategory(listing)
    return listings

def create_category_table(listings, category_name, offSeason=False):
    category_listings = [l for l in listings if l["category"] == category_name]
    if not category_listings:
        return ""

    emoji = next((cat["emoji"] for cat in CATEGORIES.values() if cat["name"] == category_name), "")
    header = f"\n\n## {emoji} {category_name} Internship Roles\n\n"
    header += "[Back to top](#summer-2026-tech-internships-by-pitt-csc--simplify)\n\n"

    # Optional callout under Data Science section
    if category_name == "Data Science, AI & Machine Learning":
        header += (
            "> 📄 Here's the [resume template](https://docs.google.com/document/d/1azvJt51U2CbpvyO0ZkICqYFDhzdfGxU_lsPQTGhsn94/edit?usp=sharing) used by Stanford CS and Pitt CSC for internship prep.\n"
            "\n"
            "> 🧠 Want to know what keywords your resume is missing for a job? Use the blue Simplify application link to instantly compare your resume to any job description.\n\n"
        )

    # Sort and format
    active = sorted([l for l in category_listings if l["active"]], key=lambda l: l["date_posted"], reverse=True)
    inactive = sorted([l for l in category_listings if not l["active"]], key=lambda l: l["date_posted"], reverse=True)

    result = header
    if active:
        result += create_md_table(active, offSeason) + "\n\n"

    if inactive:
        result += (
            "<details>\n"
            f"<summary>🗃️ Inactive roles ({len(inactive)})</summary>\n\n"
            + create_md_table(inactive, offSeason) +
            "\n\n</details>\n\n"
        )

    return result

def embedTable(listings, filepath, offSeason=False):
    # Ensure all listings have a category
    listings = ensureCategories(listings)
    listings = mark_stale_listings(listings)
    # Filter only active listings
    active_listings = filter_active(listings)
    total_active = len(active_listings)

    # Count listings by category
    category_counts = {}
    for category_info in CATEGORIES.values():
        count = len([l for l in active_listings if l["category"] == category_info["name"]])
        category_counts[category_info["name"]] = count

    # Build the category summary for the Browse section
    # Order: Software, Product, Data, Quant, Hardware, Other
    category_order = ["Software", "Product", "AI/ML/Data", "Quant", "Hardware", "Other"]
    category_links = []
    for category_key in category_order:
        if category_key in CATEGORIES:
            category_info = CATEGORIES[category_key]
            name = category_info["name"]
            emoji = category_info["emoji"]
            count = category_counts[name]
            anchor = name.lower().replace(" ", "-").replace(",", "").replace("&", "")
            category_links.append(f"{emoji} **[{name}](#-{anchor}-internship-roles)** ({count})")
    category_counts_str = "\n\n".join(category_links)

    newText = ""
    in_browse_section = False
    browse_section_replaced = False
    in_table_section = False
    table_section_replaced = False

    with open(filepath, "r") as f:
        for line in f.readlines():
            if not browse_section_replaced and line.startswith("### Browse"):
                in_browse_section = True
                newText += f"### Browse {total_active} Internship Roles by Category\n\n{category_counts_str}\n\n---\n"
                browse_section_replaced = True
                continue

            if in_browse_section:
                if line.startswith("---"):
                    in_browse_section = False
                continue

            if not in_table_section and "TABLE_START" in line:
                in_table_section = True
                newText += line
                newText += "\n---\n\n"
                # Add tables for each category in order
                category_order = ["Software", "Product", "AI/ML/Data", "Quant", "Hardware", "Other"]
                for category_key in category_order:
                    if category_key in CATEGORIES:
                        category_info = CATEGORIES[category_key]
                        table = create_category_table(listings, category_info["name"], offSeason)
                        if table:
                            newText += table
                continue

            if in_table_section:
                if "TABLE_END" in line:
                    in_table_section = False
                    newText += line
                continue

            if not in_browse_section and not in_table_section:
                newText += line

    with open(filepath, "w") as f:
        f.write(newText)


def customFilter(listings):
    def is_canada_only(locations):
        return all('canada' in loc.lower() for loc in locations)
    
    return [listing for listing in listings if 
            listing["active"] and 
            listing["sponsorship"] not in ["Does Not Offer Sponsorship", "U.S. Citizenship is Required"] and
            not is_canada_only(listing["locations"])]

def filterSummer(listings, year, earliest_date):
    # Convert blocked URLs to lowercase for case-insensitive comparison
    blocked_urls_lower = {url.lower() for url in BLOCKED_COMPANIES}
    
    final_listings = []
    for listing in listings:
        if listing["is_visible"] and any(f"Summer {year}" in item for item in listing["terms"]) and listing['date_posted'] > earliest_date:
            # Check if listing is from a blocked company
            company_url = listing.get("company_url", "").lower()
            if not any(blocked_url in company_url for blocked_url in blocked_urls_lower):
                final_listings.append(listing)
    
    return final_listings


def filterOffSeason(listings):
    def isOffSeason(listing):
        if not listing.get("is_visible"):
            return False
        
        terms = listing.get("terms", [])
        has_off_season_term = any(season in term for term in terms for season in ["Fall", "Winter", "Spring"])
        has_summer_term = any("Summer" in term for term in terms)

        # We don't want to include listings in the off season list if they include a Summer term
        #
        # Due to the nature of classification, there will sometimes be edge cases where an internship might
        # be included in two different seasons (e.g. Summer + Fall). More often than not though, these types of listings
        # are targeted towards people looking for summer internships.
        #
        # We can re-visit this in the future, but excluding listings with "Summer" term for better UX for now.
        return has_off_season_term and not has_summer_term

    return [listing for listing in listings if isOffSeason(listing)]


def sortListings(listings):
    oldestListingFromCompany = {}
    linkForCompany = {}

    for listing in listings:
        date_posted = listing["date_posted"]
        if listing["company_name"].lower() not in oldestListingFromCompany or oldestListingFromCompany[listing["company_name"].lower()] > date_posted:
            oldestListingFromCompany[listing["company_name"].lower()] = date_posted
        if listing["company_name"] not in linkForCompany or len(listing["company_url"]) > 0:
            linkForCompany[listing["company_name"]] = listing["company_url"]

    listings.sort(
        key=lambda x: (
            x["active"],  # Active listings first
            x['date_posted'],
            x['company_name'].lower(),
            x['date_updated']
        ),
        reverse=True
    )

    for listing in listings:
        listing["company_url"] = linkForCompany[listing["company_name"]]

    return listings


def checkSchema(listings):
    props = ["source", "company_name",
             "id", "title", "active", "date_updated", "is_visible",
             "date_posted", "url", "locations", "company_url", "terms",
             "sponsorship"]
    for listing in listings:
        for prop in props:
            if prop not in listing:
                fail("ERROR: Schema check FAILED - object with id " +
                      listing["id"] + " does not contain prop '" + prop + "'")