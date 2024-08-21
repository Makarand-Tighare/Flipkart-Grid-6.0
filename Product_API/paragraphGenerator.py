def parse_product_info(input_string):
    lines = input_string.splitlines()
    product_info = {
        "Product Name": "",
        "Description": "",
        "Current Price": "",
        "Original Price": "",
        "Discount": "",
        "Rating": "",
        "Number of Ratings": "",
        "Number of Reviews": "",
        "Highlights": [],
        "Offers": [],
        "Specifications": {}
    }

    # Parsing the string line by line
    current_section = None
    for line in lines:
        line = line.strip()
        if line.startswith("Product Name:"):
            product_info["Product Name"] = line.replace("Product Name:", "").strip()
        elif line.startswith("Description:"):
            product_info["Description"] = line.replace("Description:", "").strip()
        elif line.startswith("Current Price:"):
            product_info["Current Price"] = line.replace("Current Price:", "").strip()
        elif line.startswith("Original Price:"):
            product_info["Original Price"] = line.replace("Original Price:", "").strip()
        elif line.startswith("Discount:"):
            product_info["Discount"] = line.replace("Discount:", "").strip()
        elif line.startswith("Rating:"):
            product_info["Rating"] = line.replace("Rating:", "").strip()
        elif line.startswith("Number of Ratings:"):
            product_info["Number of Ratings"] = line.replace("Number of Ratings:", "").strip()
        elif line.startswith("Number of Reviews:"):
            product_info["Number of Reviews"] = line.replace("Number of Reviews:", "").strip()
        elif line.startswith("Highlights:"):
            current_section = "Highlights"
        elif line.startswith("Offers:"):
            current_section = "Offers"
        elif line.startswith("Specifications:"):
            current_section = "Specifications"
        elif current_section == "Highlights" and line.startswith("-"):
            product_info["Highlights"].append(line.replace("-", "").strip())
        elif current_section == "Offers" and line.startswith("-"):
            product_info["Offers"].append(line.replace("-", "").strip())
        elif current_section == "Specifications" and line.endswith(":"):
            section = line.replace(":", "").strip()
            product_info["Specifications"][section] = {}
            current_section = section
        elif current_section in product_info["Specifications"]:
            if ":" in line:
                key, value = line.split(":", 1)
                product_info["Specifications"][current_section][key.strip()] = value.strip()

    return product_info


def generate_paragraph(info):
    paragraph = []

    if info.get("Product Name"):
        paragraph.append(f"**The product name is** {info['Product Name']}.")

    if info.get("Description"):
        paragraph.append(f"**Its description is:** {info['Description']}.")

    if info.get("Current Price") and info.get("Original Price") and info.get("Discount"):
        paragraph.append(f"**It is currently priced at {info['Current Price']} after a discount of {info['Discount']} from the original price of {info['Original Price']}.**")

    if info.get("Rating") and info.get("Number of Ratings"):
        paragraph.append(f"**The product has a rating of {info['Rating']} based on {info['Number of Ratings']} ratings and {info.get('Number of Reviews', 'several')} reviews.**")

    if info.get("Highlights"):
        paragraph.append(f"**Some of the key highlights include: {', '.join(info['Highlights'])}.**")

    if info.get("Offers"):
        paragraph.append(f"**Current offers available are: {', '.join(info['Offers'])}.**")

    if info.get("**Specifications**"):
        specs = []
        for section, details in info["Specifications"].items():
            section_details = ', '.join([f"{key}: {value}" for key, value in details.items()])
            specs.append(f"{section} - {section_details}")
        paragraph.append(f"Specifications include: {', '.join(specs)}.")

    return ' '.join(paragraph)



def summarize_product_info(input_string):

    parsed_info = parse_product_info(input_string)
    output_paragraph = generate_paragraph(parsed_info)
    print(output_paragraph)
    return output_paragraph
