def summarize_product_info(input_string):
    lines = input_string.splitlines()
    paragraph = []

    current_section = None

    for line in lines:
        line = line.strip()

        if line.startswith("Product Name:"):
            product_name = line.replace("Product Name:", "").strip()
            paragraph.append(f"**The product name is** {product_name}.")

        elif line.startswith("Description:"):
            description = line.replace("Description:", "").strip()
            if description:
                paragraph.append(f"**Its description is:** {description}.")

        elif line.startswith("Current Price:"):
            current_price = line.replace("Current Price:", "").strip()

        elif line.startswith("Original Price:"):
            original_price = line.replace("Original Price:", "").strip()

        elif line.startswith("Discount:"):
            discount = line.replace("Discount:", "").strip()
            if current_price and original_price:
                paragraph.append(f"**It is currently priced at {current_price} after a discount of {discount} from the original price of {original_price}.**")

        elif line.startswith("Rating:"):
            rating = line.replace("Rating:", "").strip()

        elif line.startswith("Number of Ratings:"):
            num_ratings = line.replace("Number of Ratings:", "").strip()

        elif line.startswith("Number of Reviews:"):
            num_reviews = line.replace("Number of Reviews:", "").strip()
            if rating and num_ratings:
                paragraph.append(f"**The product has a rating of {rating} based on {num_ratings} ratings and {num_reviews or 'several'} reviews.**")

        elif line.startswith("Highlights:"):
            current_section = "Highlights"
            highlights = []

        elif line.startswith("Offers:"):
            if highlights:
                paragraph.append(f"**Some of the key highlights include: {', '.join(highlights)}.**")
            current_section = "Offers"
            offers = []

        elif line.startswith("Specifications:"):
            if offers:
                paragraph.append(f"**Current offers available are: {', '.join(offers)}.**")
            current_section = "Specifications"

        elif current_section == "Highlights" and line.startswith("-"):
            highlights.append(line.replace("-", "").strip())

        elif current_section == "Offers" and line.startswith("-"):
            offers.append(line.replace("-", "").strip())

        elif current_section == "Specifications" and line.endswith(":"):
            section = line.replace(":", "").strip()
            specs = []

        elif current_section == "Specifications" and ":" in line:
            key, value = line.split(":", 1)
            specs.append(f"{key.strip()}: {value.strip()}")

    # Handle remaining sections after loop
    if highlights:
        paragraph.append(f"**Some of the key highlights include: {', '.join(highlights)}.**")
    if offers:
        paragraph.append(f"**Current offers available are: {', '.join(offers)}.**")
    if specs:
        paragraph.append(f"**Specifications include: {', '.join(specs)}.**")

    return ' '.join(paragraph)


input_string = """Product Name: pari pari 108 Uno Card And Magic Cube 3x3 Combo Set Pack Of 2  (2 Pieces)
Description: 3x3 Speed Cube is an outstanding cube with great overall performance. It strikes a good balance between affordability and performance. Suitable for beginner and professional player The 3x3 cube has an endless amount of ways to solve it. Depending on whether you figure it out yourself or get help from tutorials.
Current Price: ₹201
Original Price: ₹349
Discount: 42 %
Rating: 3.6
Number of Ratings: 12
Number of Reviews: 1
Highlights:
  - Material: Plastic, Paper
  - Age: 3+ Years
  - Skillset: Alphabet & Number Recognition, Color & Shape Recognition, Time Management, Sensory Development, Memory Building, General Knowledge
Offers:
  - Special Price: Get extra 5% off (price inclusive of cashback/coupon)
  - Partner Offer: Make a purchase and enjoy a surprise cashback/ coupon that you can redeem later!
  - Bank Offer: Get ₹50 Instant Discount on first Flipkart UPI transaction on order of ₹200 and above
  - Bank Offer: 5% Unlimited Cashback on Flipkart Axis Bank Credit Card
Specifications:
  - Puzzle Features:
    - Type: Cubes
    - Ideal for: Boys, Girls
    - Minimum Age: 3 Years
    - Character: UNO
    - Material: Plastic, Paper
  - Power Features:
    - Battery Type: 0 No batteries Battery
    - Rechargeable: No
  - Additional Features:
    - Battery Operated: No
  - Product Dimensions:
    - Product Width: 7 inch
    - Product Height: 7 inch
    - Product Depth: 3 inch
    - Product Weight: 86 g
  - Box Dimensions:
    - Width: 7 inch
    - Height: 7 inch
    - Depth: 3 inch
    - Weight: 86 g
"""

# Summarize and print the product info
output_paragraph = summarize_product_info(input_string)
print(output_paragraph)
