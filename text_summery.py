from transformers import pipeline

# Initialize the summarization pipeline
summarizer = pipeline("summarization", model="Falconsai/text_summarization")

# Your text to summarize
text = """
Product Name 0: Men Printed Hooded Neck Cotton Blend Black T-Shirt
Product Url: https://www.flipkart.com/tripr-printed-men-hooded-neck-black-t-shirt/p/itm6799db09c2b82?pid=TSHGY9TCUZFGKHGA&lid=LSTTSHGY9TCUZFGKHGA5LE6SP&marketplace=FLIPKART&store=clo%2Fash%2Fank%2Fedy&srno=b_1_1&otracker=browse&fm=organic&iid=en_DqVmAVZp9JcOZ12w0LyUwrKNi5sUGGs1z5z_MLmpdhsn8nVWJDJW7QfdyfevQuxKbX7Lh8GuD2DdkJ9ZbkETFPUFjCTyOHoHZs-Z5_PS_w0%3D&ppt=None&ppn=None&ssid=hf14v6qij40000001724248641965
Price: $322
Original Price: ₹1399
Discount: 76 
Rating: None

Product Name 1: Men Solid Crew Neck Cotton Blend Green T-Shirt
Product Url: https://www.flipkart.com/being-human-solid-men-crew-neck-green-t-shirt/p/itm805831775d285?pid=TSHHYVUYC7ZUNTF8&lid=LSTTSHHYVUYC7ZUNTF8WPDEIR&marketplace=FLIPKART&store=clo%2Fash%2Fank%2Fedy&srno=b_1_5&otracker=browse&fm=organic&iid=450ce984-6f2f-4a69-9a6b-b2700ab2caad.TSHHYVUYC7ZUNTF8.SEARCH&ppt=None&ppn=None&ssid=hf14v6qij40000001724248641965
Price: $431
Original Price: ₹799
Discount: 46 
Rating: None

Product Name 2: Men Striped Round Neck Cotton Blend Green T-Shirt
Product Url: https://www.flipkart.com/roadster-striped-men-round-neck-green-t-shirt/p/itmdc30234780d60?pid=TSHHFHA8KASNRWJH&lid=LSTTSHHFHA8KASNRWJHQ5JZBM&marketplace=FLIPKART&store=clo%2Fash%2Fank%2Fedy&srno=b_1_9&otracker=browse&fm=organic&iid=450ce984-6f2f-4a69-9a6b-b2700ab2caad.TSHHFHA8KASNRWJH.SEARCH&ppt=None&ppn=None&ssid=hf14v6qij40000001724248641965
Price: $350
Original Price: ₹999
Discount: 64 
Rating: None

Product Name 3: Pack of 4 Men Solid Round Neck Polyester Black, Blue, Grey T-Shirt
Product Url: https://www.flipkart.com/vebnor-solid-men-round-neck-black-blue-grey-t-shirt/p/itma8ac88224316a?pid=TSHGQGJXHGZFUZER&lid=LSTTSHGQGJXHGZFUZERP58P3N&marketplace=FLIPKART&store=clo%2Fash%2Fank%2Fedy&srno=b_1_13&otracker=browse&fm=organic&iid=450ce984-6f2f-4a69-9a6b-b2700ab2caad.TSHGQGJXHGZFUZER.SEARCH&ppt=None&ppn=None&ssid=hf14v6qij40000001724248641965
Price: $399
Original Price: ₹999
Discount: 60 
Rating: None

Product Name 4: Pack of 3 Men Solid Round Neck Cotton Blend Dark Blue, Dark Green, Black T-Shirt
Product Url: https://www.flipkart.com/london-hills-solid-men-round-neck-dark-blue-green-black-t-shirt/p/itm23b4d6a1622a6?pid=TSHF5FYCTM8357WP&lid=LSTTSHF5FYCTM8357WPS3TERN&marketplace=FLIPKART&store=clo%2Fash%2Fank%2Fedy&srno=b_1_17&otracker=browse&fm=organic&iid=en_DqVmAVZp9JcOZ12w0LyUwrKNi5sUGGs1z5z_MLmpdht8X5U7DrmoEp8veKYka9dGM4Kz6mELn5NBSDKPW-izDQ%3D%3D&ppt=None&ppn=None&ssid=hf14v6qij40000001724248641965
Price: $499
Original Price: ₹3897
Discount: 87 
Rating: None

Product Name 5: CR Team Men Solid Polo Neck Polyester White T-Shirt
Product Url: https://www.flipkart.com/puma-solid-men-polo-neck-white-t-shirt/p/itm7a355f05bbb27?pid=TSHG54BQVHA56PZH&lid=LSTTSHG54BQVHA56PZHOBIBO0&marketplace=FLIPKART&store=clo%2Fash%2Fank%2Fedy&srno=b_1_21&otracker=browse&fm=organic&iid=en_DqVmAVZp9JcOZ12w0LyUwrKNi5sUGGs1z5z_MLmpdhugCIsFetiGboX_xSd3Q-SE15CJG3cbyjXsMyy4KdmoooE8waCTrWcncKeK_ydPfoM%3D&ppt=None&ppn=None&ssid=hf14v6qij40000001724248641965
Price: $699
Original Price: ₹1999
Discount: 65 
Rating: None

Product Name 6: Men Solid Polo Neck Cotton Blend (220 gsm) Green T-Shirt
Product Url: https://www.flipkart.com/3bros-solid-men-polo-neck-green-t-shirt/p/itm7e860cbd6041c?pid=TSHGBAWVYA8YFZX8&lid=LSTTSHGBAWVYA8YFZX8OFOOAM&marketplace=FLIPKART&store=clo%2Fash%2Fank%2Fedy&srno=b_1_25&otracker=browse&fm=organic&iid=450ce984-6f2f-4a69-9a6b-b2700ab2caad.TSHGBAWVYA8YFZX8.SEARCH&ppt=None&ppn=None&ssid=hf14v6qij40000001724248641965
Price: $339
Original Price: ₹999
Discount: 66 
Rating: None

Product Name 7: Men Colorblock Polo Neck Poly Cotton Maroon T-Shirt
Product Url: https://www.flipkart.com/dyrectdeals-colorblock-men-polo-neck-maroon-t-shirt/p/itm384be7fd67fcc?pid=TSHGMG9XUVSHGPSJ&lid=LSTTSHGMG9XUVSHGPSJYBJQA4&marketplace=FLIPKART&store=clo%2Fash%2Fank%2Fedy&srno=b_1_29&otracker=browse&fm=organic&iid=450ce984-6f2f-4a69-9a6b-b2700ab2caad.TSHGMG9XUVSHGPSJ.SEARCH&ppt=None&ppn=None&ssid=hf14v6qij40000001724248641965
Price: $299
Original Price: ₹1299
Discount: 76 
Rating: None

Product Name 8: Men Solid Polo Neck Cotton Blend (220 gsm) Green T-Shirt
Product Url: https://www.flipkart.com/3bros-solid-men-polo-neck-green-t-shirt/p/itmd0551940a1b12?pid=TSHGBBN975HVYFKH&lid=LSTTSHGBBN975HVYFKHBFPVRM&marketplace=FLIPKART&store=clo%2Fash%2Fank%2Fedy&srno=b_1_33&otracker=browse&fm=organic&iid=450ce984-6f2f-4a69-9a6b-b2700ab2caad.TSHGBBN975HVYFKH.SEARCH&ppt=None&ppn=None&ssid=hf14v6qij40000001724248641965
Price: $339
Original Price: ₹999
Discount: 66 
Rating: None

Product Name 9: Men Printed Round Neck Pure Cotton White T-Shirt
Product Url: https://www.flipkart.com/here-now-printed-men-round-neck-white-t-shirt/p/itma60929666cf67?pid=TSHFZYR74AWVGSWJ&lid=LSTTSHFZYR74AWVGSWJ2L5GIA&marketplace=FLIPKART&store=clo%2Fash%2Fank%2Fedy&srno=b_1_37&otracker=browse&fm=organic&iid=en_DqVmAVZp9JcOZ12w0LyUwrKNi5sUGGs1z5z_MLmpdhvH-cXFxI5pq2u6DFS7aL2vWKYgXMkAMhlB8Lqwte7vpA%3D%3D&ppt=None&ppn=None&ssid=hf14v6qij40000001724248641965
Price: $196
Original Price: ₹699
Discount: 71 
Rating: None

"""

# Summarize the text
summary = summarizer(text)

# Print the summary
print(summary[0]['summary_text'])
