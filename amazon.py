import uuid
from flask import Flask, render_template, abort, session, redirect, url_for, flash, request
from jinja2 import DictLoader

CURRENCY_SYMBOLS = {
    'USD': '$',
    'INR': '₹',
    'EUR': '€',
    'JPY': '¥',
    'GBP': '£'
}

# --- Data Classes ---

class Product:
    """Represents a single product in the store."""
    def __init__(self, name, price, description, category, image_urls, stock=10, rating=4.5, reviews=150, features=None, specs=None):
        self.product_id = str(uuid.uuid4())
        self.name = name
        self.price = price
        self.description = description
        self.category = category
        self.image_urls = image_urls # Now a list
        self.stock = stock
        self.rating = rating
        self.reviews = reviews
        self.features = features if features is not None else []
        self.specs = specs if specs is not None else {}

    def __str__(self):
        return f"ID: {self.product_id}\nName: {self.name}\nPrice: ${self.price:.2f}\nCategory: {self.category}"

    def update_stock(self, quantity):
        """Updates the stock level of the product."""
        if self.stock >= quantity:
            self.stock -= quantity
            return True
        print(f"Error: Not enough stock for {self.name}. Only {self.stock} available.")
        return False

class User:
    def __init__(self, email, password, name):
        self.id = str(uuid.uuid4())
        self.email = email
        self.password = password
        self.name = name

users_list = [
    User("user@example.com", "password", "Test User")
]
users_dict = {u.email: u for u in users_list}
users_by_id = {u.id: u for u in users_list}

import datetime

class Order:
    def __init__(self, user_id, items, total_price):
        self.order_id = str(uuid.uuid4())
        self.user_id = user_id
        self.items = items
        self.total_price = total_price
        self.order_date = datetime.datetime.now()

orders_list = []

# --- Flask Web Application ---

app = Flask(__name__)
# A secret key is required for session management
app.secret_key = 'a-super-secret-key-for-the-project'


@app.context_processor
def inject_session():
    return dict(
        session=session,
        currency_symbol=CURRENCY_SYMBOLS.get(session.get('currency', 'USD'), '$')
    )

@app.route('/set_locale', methods=['POST'])
def set_locale():
    session['language'] = request.form.get('language', 'en_US')
    session['currency'] = request.form.get('currency', 'USD')
    flash('Your language and currency preferences have been updated.', 'success')
    return redirect(request.referrer or url_for('home_page'))


# --- In-Memory Database ---
products_list = [
    # --- Laptops ---
    Product(
        "HP Victus 15-fb3004AX", 599.99, "A powerful gaming laptop for entry-level gamers, featuring an AMD Ryzen 5 processor and NVIDIA RTX 2050 graphics for an immersive experience.", "Laptops",
        ["https://placehold.co/600x400/1a1a1a/ffffff?text=Victus+1", "https://placehold.co/600x400/2a2a2a/ffffff?text=Victus+2", "https://placehold.co/600x400/3a3a3a/ffffff?text=Victus+3"],
        rating=4.5, reviews=120, 
        features=[
            "AMD Ryzen™ 5 8645HS processor with up to 5.0 GHz boost clock.",
            "NVIDIA® GeForce RTX™ 2050 Laptop GPU with 4 GB GDDR6 dedicated memory.",
            "15.6-inch Full HD (1920 x 1080) IPS anti-glare display with a 144 Hz refresh rate.",
            "16 GB DDR5-5600 MT/s RAM for smooth multitasking.",
            "512 GB PCIe Gen4 NVMe M.2 SSD for fast boot-up times and ample storage.",
            "Full-size, backlit keyboard in Performance Blue with a numeric keypad."
        ],
        specs={
            "Brand": "HP", "Model": "Victus 15-fb3004AX", "Screen Size": "15.6 inches", 
            "CPU": "AMD Ryzen™ 5 8645HS", "RAM": "16GB DDR5", "Storage": "512GB SSD", "GPU": "NVIDIA GeForce RTX 2050"
        }
    ),
    Product(
        "Lenovo ThinkBook 16", 750.00, "A business-focused laptop with a large 16-inch display, robust security features, and powerful processing for demanding workloads.", "Laptops",
        ["https://placehold.co/600x400/3a3a3a/ffffff?text=ThinkBook+1", "https://placehold.co/600x400/4a4a4a/ffffff?text=ThinkBook+2"],
        rating=4.6, reviews=90, 
        features=[
            "Up to 13th Gen Intel Core i7-13700H processor for high-performance computing.",
            "Integrated Intel Iris Xe graphics.",
            "16-inch WUXGA (1920 x 1200) IPS display with 16:10 aspect ratio.",
            "Up to 64GB of DDR5 RAM and up to 2TB of SSD storage.",
            "Comprehensive connectivity with Thunderbolt 4, USB-C, and Wi-Fi 6E.",
            "Enhanced security with a fingerprint reader and physical camera privacy shutter."
        ],
        specs={
            "Brand": "Lenovo", "Model": "ThinkBook 16", "Screen Size": "16 inches", 
            "CPU": "Up to 13th Gen Intel Core i7", "RAM": "Up to 64GB DDR5", "Storage": "Up to 2TB SSD", "Graphics": "Intel Iris Xe"
        }
    ),
    Product(
        "Apple 2022 MacBook Air M2 Chip, 13.6-inch Liquid Retina Display, 8GB RAM, 256GB SSD Storage, Backlit Keyboard, 1080p FaceTime HD Camera - Starlight", 
        1199.00, 
        "The redesigned MacBook Air is more portable than ever and weighs just 2.7 pounds. It’s the incredibly capable laptop that lets you work, play or create just about anything — anywhere.", 
        "Laptops",
        ["https://placehold.co/600x400/e0e0e0/000000?text=MacBook+Air+1", "https://placehold.co/600x400/d0d0d0/000000?text=MacBook+Air+2", "https://placehold.co/600x400/c0c0c0/000000?text=MacBook+Air+3"],
        rating=4.9, 
        reviews=1500, 
        features=[
            "STRIKINGLY THIN DESIGN — The redesigned MacBook Air is more portable than ever and weighs just 2.7 pounds. It’s the incredibly capable laptop that lets you work, play or create just about anything — anywhere.",
            "SUPERCHARGED BY M2 — Get more done faster with a next-generation 8-core CPU, up to 10-core GPU and 8GB of unified memory.",
            "UP TO 18 HOURS OF BATTERY LIFE — Go all day and into the night, thanks to the power-efficient performance of the Apple M2 chip.",
            "BIG, BEAUTIFUL DISPLAY — The 13.6-inch Liquid Retina display features over 500 nits of brightness, P3 wide color and support for 1 billion colors for vibrant images and incredible detail.",
            "ADVANCED CAMERA AND AUDIO — Look sharp and sound great with a 1080p FaceTime HD camera, three-mic array and four-speaker sound system with Spatial Audio.",
            "VERSATILE CONNECTIVITY — MacBook Air features a MagSafe charging port, two Thunderbolt ports, and a 3.5 mm headphone jack."
        ], 
        specs={
            "Brand": "Apple",
            "Model Name": "MacBook Air",
            "Screen Size": "13.6 Inches",
            "Color": "Starlight",
            "CPU Model": "Apple M2",
            "Ram Memory Installed Size": "8 GB",
            "Operating System": "macOS",
            "Special Feature": "Backlit Keyboard, Portable, Thin",
            "Graphics Card Description": "Integrated",
            "CPU Speed": "3.49 GHz",
            "Hard Disk Description": "SSD",
            "Resolution": "2560 x 1664",
            "What's in the box": "MacBook Air, 30W USB-C Power Adapter, USB-C to MagSafe 3 Cable",
            "Warranty": "1 Year Apple Warranty"
        }
    ),
    Product(
        "Asus Zenbook 14 OLED (2025)", 1150.00, "A premium OLED ultrabook with a stunning 2.8K 120Hz display, powered by the latest Intel Core Ultra processors for a balance of performance and portability.", "Laptops",
        ["https://placehold.co/600x400/888888/ffffff?text=Zenbook+14", "https://placehold.co/600x400/999999/ffffff?text=Zenbook+14+OLED"],
        rating=4.8, reviews=450, 
        features=[
            "14-inch 2.8K (2880 x 1800) ASUS Lumina OLED display with 120Hz refresh rate.",
            "Powered by Intel Core Ultra 7 or Core Ultra 9 processors with integrated NPU for AI tasks.",
            "Up to 32 GB LPDDR5x RAM and up to 1 TB PCIe Gen 4 SSD.",
            "Lightweight and durable CNC-milled aluminum chassis, MIL-STD 810H tested.",
            "Two Thunderbolt 4 ports, USB 3.2 Gen 1 Type-A, and HDMI 2.1.",
            "FHD camera with IR for Windows Hello and a privacy shutter."
        ],
        specs={
            "Brand": "Asus", "Model": "Zenbook 14 OLED (2025)", "Screen Size": "14 inches", 
            "Resolution": "2880 x 1800", "CPU": "Intel Core Ultra 7/9", "RAM": "Up to 32GB LPDDR5x", "Storage": "Up to 1TB SSD"
        }
    ),
    Product(
        "Dell G15 5530 Gaming Laptop", 1200.00, "A powerful gaming laptop with a high-refresh-rate display, 13th Gen Intel Core processors, and NVIDIA GeForce RTX 40-series graphics.", "Laptops",
        ["https://placehold.co/600x400/ff0000/ffffff?text=Dell+G15", "https://placehold.co/600x400/cc0000/ffffff?text=Dell+G15+Gaming"],
        rating=4.7, reviews=800, 
        features=[
            "13th Gen Intel Core i5, i7, or i9 processors for high-end gaming performance.",
            "NVIDIA GeForce RTX 3050, 4050, or 4060 Laptop GPUs.",
            "15.6-inch FHD (1920 x 1080) display with 120Hz or 165Hz refresh rate options.",
            "Up to 64GB of DDR5 memory and dual SSD slots.",
            "Cryo-Tech cooling system for optimal thermal performance.",
            "4-zone RGB backlit keyboard and 720p HD camera."
        ],
        specs={
            "Brand": "Dell", "Model": "G15 5530", "Screen Size": "15.6 inches", 
            "CPU": "Up to 13th Gen Intel Core i9", "GPU": "Up to NVIDIA RTX 4060", "RAM": "Up to 64GB DDR5", "Storage": "Up to 2TB SSD"
        }
    ),
    Product(
        "Lenovo LOQ 15IAX9 Gaming Laptop", 600.00, "A budget-friendly gaming laptop with an Intel Core i5 processor, NVIDIA RTX 3050 graphics, and a 144Hz display for aspiring gamers.", "Laptops",
        ["https://placehold.co/600x400/0000ff/ffffff?text=Lenovo+LOQ"],
        rating=4.3, reviews=300, 
        features=[
            "12th Generation Intel Core i5-12450HX processor.",
            "NVIDIA GeForce RTX 3050 with 6GB GDDR6 memory.",
            "15.6-inch FHD (1920x1080) IPS display with 144Hz refresh rate and G-SYNC.",
            "Up to 32GB of DDR5 4800MHz RAM.",
            "Hyperchamber thermal design for efficient cooling.",
            "Lenovo AI Engine+ with LA1 AI chip for optimized performance."
        ],
        specs={
            "Brand": "Lenovo", "Model": "LOQ 15IAX9", "Screen Size": "15.6 inches", 
            "CPU": "Intel Core i5-12450HX", "GPU": "NVIDIA RTX 3050", "RAM": "Up to 32GB DDR5", "Storage": "Up to 2TB SSD"
        }
    ),

    # --- Watches ---
    Product(
        "Casio MRW-200H", 45.00, "A robust and versatile analog watch with a diver-style look, 100-meter water resistance, and a day-date display, making it perfect for casual and active lifestyles.", "Watches",
        ["https://placehold.co/600x400/111111/ffffff?text=Casio+Sport"],
        rating=4.6, reviews=15000, 
        features=[
            "100M Water Resistance, suitable for swimming and snorkeling.",
            "Bi-directional rotating bezel for time-tracking.",
            "Day and date display at the 3 o’clock position.",
            "Luminous hands for visibility in low-light conditions.",
            "Lightweight resin case and band for durability and comfort."
        ],
        specs={
            "Brand": "Casio", "Model": "MRW-200H", "Movement": "Quartz", "Water Resistance": "100m", 
            "Case Material": "Resin", "Crystal": "Resin Glass", "Battery Life": "Approx. 3 years"
        }
    ),
    Product(
        "Timex Weekender", 55.00, "A classic and versatile watch with a simple, readable dial and easily interchangeable straps, perfect for everyday casual wear.", "Watches",
        ["https://placehold.co/600x400/f5f5dc/000000?text=Timex+Weekender"],
        rating=4.5, reviews=22000, 
        features=[
            "INDIGLO® Night-Light for easy reading in the dark.",
            "Interchangeable slip-thru straps for ultimate versatility.",
            "Full Arabic numerals and 24-hour military time.",
            "Durable chrome-finished brass case and mineral glass crystal.",
            "Water resistant to 30 meters (100 feet)."
        ],
        specs={
            "Brand": "Timex", "Model": "Weekender", "Movement": "Quartz", "Case Material": "Brass", 
            "Lug Width": "20mm", "Water Resistance": "30m", "Special Feature": "INDIGLO® Night-Light"
        }
    ),
    Product(
        "Casio Edifice Chronograph", 150.00, "A stylish and functional steel chronograph that blends a sporty design with innovative technology, ideal for both professional and casual settings.", "Watches",
        ["https://placehold.co/600x400/cccccc/000000?text=Edifice+Watch"],
        rating=4.7, reviews=1800, 
        features=[
            "1/20-second stopwatch and tachymeter for precise timing.",
            "Tough Solar technology for battery charging via light exposure.",
            "Bluetooth connectivity for smartphone linking and automatic time adjustment.",
            "Water resistant to 100 meters (10 bar).",
            "Durable stainless steel case and mineral glass."
        ],
        specs={
            "Brand": "Casio", "Model": "Edifice Chronograph", "Movement": "Quartz (Solar)", "Water Resistance": "100m", 
            "Case Material": "Stainless Steel", "Connectivity": "Bluetooth"
        }
    ),
    Product(
        "Seiko 5 Sports Automatic", 300.00, "A reliable and durable automatic watch with a classic design, featuring Seiko's in-house 4R36 movement with hacking and hand-winding capabilities.", "Watches",
        ["https://placehold.co/600x400/333333/ffffff?text=Seiko+5"],
        rating=4.8, reviews=2500, 
        features=[
            "Automatic Caliber 4R36 movement with a 41-hour power reserve.",
            "Day-date display at the 3 o'clock position.",
            "Water resistant to 100 meters (10 bar).",
            "Recessed crown at the 4 o'clock position for comfort.",
            "Durable stainless steel case and Hardlex crystal."
        ],
        specs={
            "Brand": "Seiko", "Model": "5 Sports Automatic", "Movement": "Automatic (4R36)", "Case Material": "Stainless Steel", 
            "Water Resistance": "100m", "Crystal": "Hardlex"
        }
    ),
    Product(
        "Omega Seamaster Diver 300M", 5400.00, "A legendary dive watch combining advanced technology with a sleek design, featuring a METAS-certified Master Chronometer movement and a signature wave-patterned ceramic dial.", "Watches",
        ["https://placehold.co/600x400/003366/ffffff?text=Seamaster"],
        rating=4.9, reviews=800, 
        features=[
            "OMEGA Master Chronometer Calibre 8800 with a 55-hour power reserve.",
            "Water resistant to 300 meters (1000 feet).",
            "Helium escape valve for professional diving.",
            "Unidirectional rotating bezel with a ceramic insert.",
            "Domed sapphire crystal with anti-reflective treatment on both sides."
        ],
        specs={
            "Brand": "Omega", "Model": "Seamaster Diver 300M", "Movement": "Automatic (Co-Axial Master Chronometer)", "Water Resistance": "300m", 
            "Case Material": "Stainless Steel", "Crystal": "Sapphire"
        }
    ),
    Product(
        "Titan Neo Analog Watch", 80.00, "An elegant and stylish analog watch from a popular Indian brand, featuring a classic design and reliable quartz movement, suitable for both casual and formal occasions.", "Watches",
        ["https://placehold.co/600x400/404040/ffffff?text=Titan+Neo"],
        rating=4.5, reviews=1200, 
        features=[
            "Reliable and precise quartz movement.",
            "Water resistant to 50 meters (5 ATM).",
            "Durable metal case and mineral glass dial.",
            "Available with leather or stainless steel straps.",
            "Many models include a date display and multifunction dials."
        ],
        specs={
            "Brand": "Titan", "Model": "Neo Analog Watch", "Movement": "Quartz", "Water Resistance": "50m", 
            "Case Material": "Metal", "Strap Material": "Leather or Stainless Steel"
        }
    ),

    # --- Smartwatches ---
    Product(
        "Redmi Watch 5 Active", 60.00, "A budget-friendly smartwatch with a large 2-inch LCD, Bluetooth calling, and over 140 workout modes, offering a great balance of features and affordability.", "Smartwatches",
        ["https://placehold.co/600x400/ff4500/ffffff?text=Redmi+Watch+5"],
        rating=4.3, reviews=4500, 
        features=[
            "2-inch square LCD with up to 500 nits brightness.",
            "Bluetooth 5.3 connectivity with support for Bluetooth calling.",
            "Over 140 workout modes with automatic detection for common activities.",
            "24-hour heart rate and blood oxygen (SpO2) monitoring.",
            "Up to 18 days of typical use time with a 470mAh battery.",
            "5ATM water resistance."
        ],
        specs={
            "Brand": "Redmi", "Model": "Watch 5 Active", "Display": "2-inch LCD", "Compatibility": "Android/iOS", 
            "Water Resistance": "5ATM", "Connectivity": "Bluetooth 5.3"
        }
    ),
    Product(
        "Samsung Galaxy Watch 8", 349.99, "A premium smartwatch with a sleek design, robust performance, and advanced health features, including ECG, blood pressure monitoring, and AI-powered insights.", "Smartwatches",
        ["https://placehold.co/600x400/555555/ffffff?text=Galaxy+Watch+8"],
        rating=4.7, reviews=3200, 
        features=[
            "Super AMOLED display with up to 3,000 nits peak brightness.",
            "Powered by the Exynos W1000 (3nm) penta-core chipset.",
            "Advanced health tracking with ECG, blood pressure, SpO2, and skin temperature sensors.",
            "AI-powered insights, including an Energy Score and personalized wellness tips.",
            "Built-in Google Gemini for natural voice commands and complex tasks.",
            "IP68 dust and water resistance (5ATM) and MIL-STD-810H compliant."
        ],
        specs={
            "Brand": "Samsung", "Model": "Galaxy Watch 8", "OS": "Wear OS 6", "Compatibility": "Android", 
            "Processor": "Exynos W1000", "Display": "Super AMOLED"
        }
    ),
    Product(
        "Apple Watch Ultra 3", 799.00, "The ultimate sports and adventure watch with a rugged titanium case, advanced health and fitness tracking, and built-in satellite communications for emergency situations.", "Smartwatches",
        ["https://placehold.co/600x400/f5f5f5/000000?text=Apple+Watch+Ultra"],
        rating=4.9, reviews=1800, 
        features=[
            "1.98-inch Always-On Retina LTPO3 OLED display with up to 3,000 nits peak brightness.",
            "Powered by the S10 chip with a 64-bit dual-core processor.",
            "Advanced health sensors, including ECG, blood oxygen, and wrist temperature.",
            "Built-in satellite communications for Emergency SOS.",
            "Water-resistant to 100 meters and suitable for recreational scuba diving.",
            "Customizable Action button for quick access to your favorite features."
        ],
        specs={
            "Brand": "Apple", "Model": "Watch Ultra 3", "OS": "watchOS 26", "Compatibility": "iOS", 
            "Case Material": "Titanium", "Connectivity": "Cellular + Wi-Fi"
        }
    ),
    Product(
        "Google Pixel Watch 3", 400.00, "A stylish and intelligent smartwatch with deep integration into the Google and Pixel ecosystem, featuring advanced fitness tracking and a brighter display.", "Smartwatches",
        ["https://placehold.co/600x400/4285F4/ffffff?text=Pixel+Watch+3"],
        rating=4.6, reviews=1100, 
        features=[
            "Actua AMOLED LTPO display with a peak brightness of 2,000 nits.",
            "Powered by the Qualcomm Snapdragon Wear 5100 processor.",
            "Advanced fitness tracking with Daily Readiness, Cardio Load, and Target Load tools.",
            "Loss of Pulse Detection feature for emergency situations.",
            "Deep integration with Google services, including Google TV and Nest Camera controls.",
            "Ultra-wideband support for unlocking your phone."
        ],
        specs={
            "Brand": "Google", "Model": "Pixel Watch 3", "OS": "Wear OS 5", "Compatibility": "Android", 
            "Processor": "Snapdragon Wear 5100", "Display": "Actua AMOLED LTPO"
        }
    ),

    # --- Monitors ---
    Product(
        "ASUS ROG Swift OLED PG27UCDM", 1299.00, "A top-tier 27-inch 4K QD-OLED gaming monitor with a 240Hz refresh rate, offering stunning visuals and a competitive edge for serious gamers.", "Monitors",
        ["https://placehold.co/600x400/ff0000/ffffff?text=ROG+Monitor"],
        rating=4.9, reviews=250, 
        features=[
            "26.5-inch 4K UHD (3840 x 2160) QD-OLED panel for incredible contrast and vibrant colors.",
            "240Hz refresh rate and 0.03ms (GTG) response time for ultra-smooth gameplay.",
            "Supports both AMD FreeSync Premium Pro and NVIDIA G-SYNC for tear-free gaming.",
            "Extensive connectivity with DisplayPort 2.1, HDMI 2.1, and USB-C with 90W Power Delivery.",
            "Built-in KVM switch and ASUS OLED Care to prevent burn-in."
        ],
        specs={
            "Brand": "ASUS", "Model": "ROG Swift OLED PG27UCDM", "Screen Size": "27 inches", "Resolution": "3840 x 2160", 
            "Panel Type": "QD-OLED", "Refresh Rate": "240Hz", "Response Time": "0.03ms"
        }
    ),
    Product(
        "Dell U2725QE Office Monitor", 650.00, "A professional 27-inch 4K monitor designed for productivity, featuring an IPS Black panel for exceptional color and contrast, and extensive connectivity options.", "Monitors",
        ["https://placehold.co/600x400/0000ff/ffffff?text=Dell+Monitor"],
        rating=4.8, reviews=400, 
        features=[
            "27-inch 4K UHD (3840 x 2160) IPS Black panel with a 120Hz refresh rate.",
            "DisplayHDR 600 certified with a 3000:1 contrast ratio.",
            "Thunderbolt 4 hub monitor with 140W power delivery.",
            "Built-in KVM switch and 2.5GbE RJ45 Ethernet port.",
            "ComfortView Plus for reduced blue light emissions."
        ],
        specs={
            "Brand": "Dell", "Model": "U2725QE", "Screen Size": "27 inches", "Resolution": "3840 x 2160", 
            "Panel Type": "IPS Black", "Refresh Rate": "120Hz", "Connectivity": "Thunderbolt 4"
        }
    ),
    Product(
        "Dell S3222DGM Gaming Monitor", 300.00, "A budget-friendly 32-inch 1440p curved gaming monitor with a high refresh rate and excellent contrast, perfect for immersive gaming experiences.", "Monitors",
        ["https://placehold.co/600x400/aaaaaa/000000?text=Dell+Gaming"],
        rating=4.6, reviews=3500, 
        features=[
            "31.5-inch QHD (2560 x 1440) curved VA panel with a 1800R curvature.",
            "165Hz refresh rate and 1ms MPRT for smooth, responsive gameplay.",
            "AMD FreeSync Premium and G-Sync Compatible for tear-free visuals.",
            "99% sRGB color gamut and a 3000:1 contrast ratio.",
            "Height and tilt adjustable stand for ergonomic comfort."
        ],
        specs={
            "Brand": "Dell", "Model": "S3222DGM", "Screen Size": "32 inches", "Resolution": "2560 x 1440", 
            "Panel Type": "VA", "Refresh Rate": "165Hz", "Curvature": "1800R"
        }
    ),

    # --- Headphones ---
    Product(
        "Sony WH-1000XM6", 399.99, "Industry-leading noise-canceling wireless headphones with studio-quality sound, a new faster processor, and a comfortable, foldable design.", "Headphones",
        ["https://placehold.co/600x400/000000/ffffff?text=Sony+XM6"],
        rating=4.9, reviews=8000, 
        features=[
            "HD Noise Canceling Processor QN3 for optimized noise cancellation.",
            "DSEE Extreme™ to upscale compressed music files in real time.",
            "Up to 30 hours of battery life with Noise Cancelling ON.",
            "LE Audio support for ultra-low latency gaming.",
            "Multipoint connection to switch between two devices seamlessly."
        ],
        specs={
            "Brand": "Sony", "Model": "WH-1000XM6", "Type": "Over-Ear, Wireless", "ANC": "Yes", 
            "Bluetooth": "5.3", "Battery Life": "Up to 30 hours (ANC on)"
        }
    ),
    Product(
        "Bowers & Wilkins Px7 S3", 429.00, "Premium wireless headphones with engaging sound, advanced noise cancellation, and a refined, comfortable design for an exceptional listening experience.", "Headphones",
        ["https://placehold.co/600x400/666666/ffffff?text=B%26W+Px7"],
        rating=4.7, reviews=900, 
        features=[
            "Custom-designed 40mm bio-cellulose drivers for rich, detailed sound.",
            "Advanced hybrid noise-cancelling circuitry with 8 microphones.",
            "Supports aptX™ Lossless for high-fidelity wireless audio.",
            "Up to 30 hours of playback with Active Noise Cancellation (ANC) on.",
            "Bluetooth multipoint for connecting to two devices simultaneously."
        ],
        specs={
            "Brand": "Bowers & Wilkins", "Model": "Px7 S3", "Type": "Over-Ear, Wireless", "ANC": "Adaptive", 
            "Bluetooth Codecs": "aptX Lossless, aptX HD, AAC, SBC", "Battery Life": "Up to 30 hours"
        }
    ),
    Product(
        "Sennheiser HD 660S2 Wired Headphones", 599.00, "Audiophile-grade open-back wired headphones designed for high-fidelity audio, featuring a new 38mm transducer for a natural, warm sound with extended sub-bass.", "Headphones",
        ["https://placehold.co/600x400/333333/ffffff?text=Sennheiser+HD660S2"],
        rating=4.8, reviews=400, 
        features=[
            "Open-back design for a natural and spacious soundstage.",
            "38mm dynamic drivers with an ultra-light aluminum voice coil.",
            "300-ohm impedance for optimal performance with headphone amplifiers.",
            "Plush velour ear pads for maximum comfort during long listening sessions.",
            "Includes two detachable cables (6.3mm and 4.4mm balanced)."
        ],
        specs={
            "Brand": "Sennheiser", "Model": "HD 660S2", "Type": "Open-back, Wired", "Impedance": "300 Ohm", 
            "Frequency Response": "8 Hz – 41,500 Hz", "Driver Type": "Dynamic, 38mm"
        }
    ),

    # --- Bags ---
    Product(
        "Timbuk2 Authority Laptop Backpack Deluxe", 139.00, "A feature-rich and durable backpack designed for professionals and commuters, offering extensive organization, comfort, and a sleek, professional aesthetic.", "Bags",
        ["https://placehold.co/600x400/888888/ffffff?text=Timbuk2+Bag", "https://placehold.co/600x400/999999/ffffff?text=Timbuk2+Interior"],
        rating=4.7, reviews=950, 
        features=[
            "Padded laptop sleeve fits up to a 17-inch laptop and is accessible from inside and outside the pack.",
            "Air mesh ventilated back panel and padded shoulder straps for all-day comfort.",
            "Luggage pass-through for easy attachment to rolling luggage.",
            "Water-resistant exterior and waterproof boot on the bottom for protection against the elements.",
            "Extensive interior organization with multiple pockets and a key clip."
        ],
        specs={
            "Brand": "Timbuk2", "Model": "Authority Laptop Backpack Deluxe", "Type": "Backpack", "Capacity": "20L", 
            "Material": "100% recycled nylon", "Laptop Compatibility": "Up to 17 inches"
        }
    ),
    Product(
        "Cotopaxi Allpa 35L Travel Pack", 200.00, "A thoughtfully designed and durable travel backpack built for organized, carry-on travel, featuring a suitcase-style opening and versatile carry options.", "Bags",
        ["https://placehold.co/600x400/4682b4/ffffff?text=Cotopaxi+Allpa", "https://placehold.co/600x400/5a91d2/ffffff?text=Cotopaxi+Open"],
        rating=4.8, reviews=1100, 
        features=[
            "35-liter capacity, carry-on compatible for most major airlines.",
            "Suitcase-style, full-wrap zipper opening for easy packing.",
            "Padded laptop sleeve fits up to a 15-inch laptop.",
            "Tuckable shoulder straps and hip belt for multiple carrying options.",
            "Durable 840D TPU-coated nylon shell for weather and wear resistance."
        ],
        specs={
            "Brand": "Cotopaxi", "Model": "Allpa 35L Travel Pack", "Type": "Travel Backpack", "Capacity": "35L", 
            "Material": "TPU-coated 840D nylon", "Laptop Compatibility": "Up to 15 inches"
        }
    ),
    Product(
        "Patagonia Black Hole Duffel 55L", 159.00, "A durable, weather-resistant, and versatile duffel bag designed for weekend trips or extended travel, made with 100% recycled materials.", "Bags",
        ["https://placehold.co/600x400/ff6600/ffffff?text=Patagonia+Duffel", "https://placehold.co/600x400/cc5500/ffffff?text=Patagonia+Duffel+Open"],
        rating=4.8, reviews=1200, 
        features=[
            "55-liter capacity, perfect for weekend trips.",
            "Made from 100% recycled polyester ripstop with a recycled TPU-film laminate.",
            "Padded, removable shoulder straps allow it to be carried as a backpack.",
            "Large main compartment with a zippered side pocket and mesh interior lid pocket.",
            "Stuffs into its own side pocket for compact storage."
        ],
        specs={
            "Brand": "Patagonia", "Model": "Black Hole Duffel 55L", "Type": "Duffel Bag", "Capacity": "55L", 
            "Material": "100% recycled polyester ripstop", "Sustainability": "Fair Trade Certified™ factory"
        }
    ),
    Product(
        "Osprey Transporter Duffel 40L", 120.00, "A rugged yet lightweight, carry-on-sized duffel bag designed for adventure travel, featuring a stowaway harness system and highly water-resistant fabric.", "Bags",
        ["https://placehold.co/600x400/3cb371/ffffff?text=Osprey+Transporter"],
        rating=4.7, reviews=800, 
        features=[
            "40-liter capacity, meets carry-on size restrictions for most airlines.",
            "Padded, stowaway harness system for backpack-style carrying.",
            "Large, lockable U-zip access to the main compartment.",
            "Weather-protected main compartment zip path with an overlapping rain flap.",
            "Made with 100% recycled high-tenacity nylon with a carbonate coating."
        ],
        specs={
            "Brand": "Osprey", "Model": "Transporter Duffel 40L", "Type": "Duffel Bag", "Capacity": "40L", 
            "Material": "Recycled high-tenacity nylon", "Carry-On": "Yes"
        }
    ),


    # --- Smartphones ---
    Product("Moto G96 5G", 175.00, "A mid-range 5G smartphone offering a blend of style and performance, with a 144Hz pOLED 3D curved display, a 50MP camera with OIS, and a 5500mAh battery with 68W fast charging.", "Smartphones", ["https://placehold.co/600x400/007bff/fff?text=Moto+G96+5G"], rating=4.2, reviews=5000, 
        features=[
            "6.67-inch FHD+ pOLED 3D Curved Display with 144Hz refresh rate.",
            "Qualcomm Snapdragon 7s Gen 2 processor for smooth performance.",
            "50MP main camera with OIS and an 8MP ultra-wide/macro lens.",
            "5500mAh battery with 68W TurboPower fast charging.",
            "IP68 dust and water resistance."
        ],
        specs={
            "Brand": "Motorola", "Model": "Moto G96 5G", "Processor": "Snapdragon 7s Gen 2", "Display": "6.67-inch pOLED", 
            "RAM": "8GB", "Storage": "128GB/256GB", "Main Camera": "50MP with OIS"
        }
    ),
    Product("Redmi Note 14 SE 5G", 190.00, "An affordable 5G smartphone with a 120Hz AMOLED display, a 50MP camera with OIS, and a large 5110mAh battery with 45W fast charging.", "Smartphones", ["https://placehold.co/600x400/00bcd4/fff?text=Redmi+Note+14+SE+5G"], rating=4.3, reviews=7200, 
        features=[
            "6.67-inch FHD+ AMOLED display with a 120Hz refresh rate.",
            "MediaTek Dimensity 7025-Ultra processor.",
            "50MP Sony IMX882 main camera with OIS.",
            "5110mAh battery with 45W wired fast charging.",
            "Dual stereo speakers with Dolby Atmos."
        ],
        specs={
            "Brand": "Redmi", "Model": "Note 14 SE 5G", "Display": "6.67-inch AMOLED", "Processor": "Dimensity 7025-Ultra", 
            "RAM": "6GB/8GB", "Storage": "128GB/256GB", "Main Camera": "50MP with OIS"
        }
    ),
    Product("Samsung Galaxy A35 5G", 260.00, "A mid-range smartphone with a premium design, a 120Hz Super AMOLED display, a 50MP main camera with OIS, and long-term software support.", "Smartphones", ["https://placehold.co/600x400/4caf50/fff?text=Galaxy+A35+5G"], rating=4.5, reviews=8900, 
        features=[
            "6.6-inch Super AMOLED display with a 120Hz refresh rate.",
            "Exynos 1380 processor for reliable performance.",
            "50MP main camera with OIS, an 8MP ultra-wide, and a 5MP macro lens.",
            "5000mAh battery with 25W fast charging support.",
            "IP67 dust and water resistance and Samsung Knox security."
        ],
        specs={
            "Brand": "Samsung", "Model": "Galaxy A35 5G", "OS": "Android 14", "Processor": "Exynos 1380", 
            "Display": "6.6-inch Super AMOLED", "RAM": "6GB/8GB", "Storage": "128GB/256GB"
        }
    ),
    Product("Google Pixel 9", 950.00, "A flagship smartphone with a clean Android experience, a powerful Tensor G4 processor, and an advanced AI-powered camera system for stunning photos.", "Smartphones", ["https://placehold.co/600x400/03a9f4/fff?text=Google+Pixel+9"], rating=4.8, reviews=1100, 
        features=[
            "6.3-inch Actua OLED display with a 120Hz refresh rate.",
            "Google Tensor G4 processor with Gemini AI integration.",
            "50MP wide-angle primary camera and a 48MP ultra-wide angle camera.",
            "4700mAh battery with fast wired and wireless charging.",
            "7 years of OS, security, and Pixel Drop updates."
        ],
        specs={
            "Brand": "Google", "Model": "Pixel 9", "OS": "Android 14", "Processor": "Google Tensor G4", 
            "Display": "6.3-inch Actua OLED", "RAM": "12GB", "Storage": "128GB/256GB"
        }
    ),
    Product(
        "Apple iPhone 16, 128GB, Black - Unlocked, 6.1-inch Super Retina XDR Display, A18 Chip with AI, Advanced Dual-Camera System", 
        1600.00, 
        "The iPhone 16 features the powerful A18 chip with next-gen AI capabilities, a more advanced dual-camera system with Spatial Video capture, and a durable, beautiful design.", 
        "Smartphones", 
        ["https://placehold.co/600x400/e0e0e0/000?text=iPhone+16"], 
        rating=4.9, 
        reviews=1800, 
        features=[
            "SPATIAL VIDEO CAPTURE: The new vertical camera alignment isn't just a design choice—it lets you capture immersive Spatial Videos that you can relive in the Apple Vision Pro.",
            "A18 CHIP WITH APPLE INTELLIGENCE: The A18 chip brings powerhouse performance, optimizing the phone for next-generation generative AI features and offering incredible efficiency for longer battery life.",
            "ADVANCED DUAL-CAMERA SYSTEM: A 48MP Main camera and a new 12MP Ultra Wide with macro capabilities let you take super-high-resolution photos and get even closer to your subjects. The Photonic Engine and Smart HDR 5 ensure your photos have fantastic detail and color.",
            "DURABLE DESIGN WITH CERAMIC SHIELD: Featuring a beautiful and durable aluminum design with color-infused glass and the tough Ceramic Shield front, which is tougher than any smartphone glass.",
            "ACTION BUTTON & CAMERA CONTROL: The new Action button provides quick access to your favorite feature, while the dedicated Camera Control button makes capturing the perfect shot easier than ever.",
            "WI-FI 7 AND USB-C: Get the fastest wireless speeds available with Wi-Fi 7 and enjoy the universal standard of USB-C for charging and data transfer."
        ], 
        specs={
            "Brand": "Apple",
            "Model Name": "iPhone 16",
            "Operating System": "iOS 18",
            "Ram Memory Installed Size": "8 GB",
            "CPU Model": "Apple A18",
            "Memory Storage Capacity": "128 GB",
            "Screen Size": "6.1 Inches",
            "Display Technology": "Super Retina XDR OLED",
            "Resolution": "2556 x 1179",
            "Refresh Rate": "60 Hz",
            "Wireless Carrier": "Unlocked for All Carriers",
            "Connectivity Technology": "Wi-Fi 7, Bluetooth 5.3, 5G, NFC",
            "Color": "Black",
            "What's in the box": "iPhone with iOS 18, USB-C to USB-C Cable, Documentation",
            "Warranty": "1 Year US Warranty"
        }
    ),

    # --- Gaming Components (more products) ---
    Product("Intel Core i9-14900K CPU", 599.00, "Intel's flagship desktop processor with a hybrid architecture of 24 cores and 32 threads, designed for high-end gaming, content creation, and productivity.", "Gaming Components", ["https://placehold.co/600x400/FF5733/FFF?text=i9+CPU"], rating=4.9, reviews=850, 
        features=[
            "24 cores (8 Performance-cores and 16 Efficient-cores) and 32 threads.",
            "Up to 6.0 GHz max turbo frequency with Intel Thermal Velocity Boost.",
            "Unlocked for overclocking to push performance even further.",
            "Supports both DDR5 and DDR4 memory.",
            "Integrated Intel UHD Graphics 770."
        ],
        specs={
            "Brand": "Intel", "Model": "Core i9-14900K", "Cores": "24", "Threads": "32", 
            "Max Turbo Frequency": "6.0 GHz", "Cache": "36 MB Intel Smart Cache"
        }
    ),
    Product("NVIDIA GeForce RTX 4090 GPU", 1599.00, "The ultimate gaming GPU with 24GB of GDDR6X memory, powered by the NVIDIA Ada Lovelace architecture for a quantum leap in performance and AI-powered graphics.", "Gaming Components", ["https://placehold.co/600x400/C70039/FFF?text=RTX+4090"], rating=4.9, reviews=1500, 
        features=[
            "24GB of GDDR6X VRAM for handling the most demanding games and creative workloads.",
            "NVIDIA DLSS 3 for a massive boost in performance.",
            "3rd generation RT Cores for realistic and immersive ray tracing.",
            "4th generation Tensor Cores for AI-powered graphics and machine learning.",
            "Dual AV1 encoders for high-quality streaming and video encoding."
        ],
        specs={
            "Brand": "NVIDIA", "Model": "GeForce RTX 4090", "Memory": "24GB GDDR6X", "CUDA Cores": "16,384", 
            "Boost Clock": "2.52 GHz", "Architecture": "Ada Lovelace"
        }
    ),
    Product("ASUS ROG Strix Z790-E Motherboard", 399.00, "A high-end ATX motherboard for Intel CPUs with a robust power delivery system, extensive connectivity, and a host of DIY-friendly features for enthusiast builders.", "Gaming Components", ["https://placehold.co/600x400/900C3F/FFF?text=Z790+Mobo"], rating=4.7, reviews=450, 
        features=[
            "18+1 power stage design for stable power delivery.",
            "Supports DDR5 RAM up to 7800 MHz (OC).",
            "One PCIe 5.0 x16 slot and five M.2 slots (one PCIe 5.0).",
            "Wi-Fi 6E and 2.5 Gigabit LAN for high-speed networking.",
            "ASUS Q-Latch and Q-Release for easy component installation."
        ],
        specs={
            "Brand": "ASUS", "Model": "ROG Strix Z790-E Gaming WiFi", "Chipset": "Intel Z790", "Socket": "LGA 1700", 
            "Form Factor": "ATX", "Memory Support": "DDR5"
        }
    ),
    Product("Corsair Vengeance DDR5 32GB RAM", 129.99, "High-performance DDR5 memory with a low-profile heat spreader, optimized for Intel motherboards with XMP 3.0 support for easy overclocking.", "Gaming Components", ["https://placehold.co/600x400/581845/FFF?text=DDR5+RAM"], rating=4.8, reviews=2500, 
        features=[
            "32GB (2x16GB) kit of high-speed DDR5 memory.",
            "Available in speeds up to 7000MHz.",
            "Onboard voltage regulation for stable overclocking.",
            "Compact aluminum heat spreader for wide compatibility.",
            "Optimized for Intel 600, 700, and 800 Series motherboards."
        ],
        specs={
            "Brand": "Corsair", "Model": "Vengeance DDR5", "Capacity": "32GB (2x16GB)", "Type": "DDR5", 
            "Speed": "Up to 7000MHz", "CAS Latency": "Varies by speed"
        }
    ),
    Product("Samsung 990 Pro 2TB NVMe SSD", 179.99, "An ultra-fast NVMe SSD with sequential read speeds up to 7,450 MB/s, designed for high-end gaming, content creation, and data analysis.", "Gaming Components", ["https://placehold.co/600x400/FFC300/000?text=2TB+SSD"], rating=4.9, reviews=3200, 
        features=[
            "Sequential read speeds up to 7,450 MB/s and write speeds up to 6,900 MB/s.",
            "PCIe 4.0 interface and NVMe 2.0 support.",
            "Intelligent TurboWrite 2.0 for consistent performance under heavy workloads.",
            "Dynamic Thermal Guard Technology to maintain optimal temperature.",
            "Optimized for PS5 and DirectStorage PC games."
        ],
        specs={
            "Brand": "Samsung", "Model": "990 Pro", "Capacity": "2TB", "Interface": "NVMe PCIe 4.0", 
            "Read Speed": "Up to 7,450 MB/s", "Write Speed": "Up to 6,900 MB/s"
        }
    ),
    Product("Corsair RM1000e PSU", 149.99, "A 1000W fully modular ATX power supply with 80 PLUS Gold certification, designed for modern high-performance PC builds with a native 12V-2x6 connector.", "Gaming Components", ["https://placehold.co/600x400/DAF7A6/000?text=1000W+PSU"], rating=4.7, reviews=700, 
        features=[
            "1000W of continuous power.",
            "80 PLUS Gold certified for up to 90% efficiency.",
            "Fully modular cabling for reduced clutter and improved airflow.",
            "120mm rifle bearing fan with a Zero RPM Fan Mode for silent operation at low loads.",
            "ATX 3.1 and PCIe 5.1 compliant."
        ],
        specs={
            "Brand": "Corsair", "Model": "RM1000e", "Wattage": "1000W", "Efficiency": "80 PLUS Gold", 
            "Modularity": "Fully Modular", "Form Factor": "ATX"
        }
    ),
    Product("Lian Li O11 Dynamic EVO Case", 169.00, "A popular mid-tower PC case with a dual-chamber design, extensive cooling support, and a reversible chassis for a left or right-side view of the interior.", "Gaming Components", ["https://placehold.co/600x400/FFC0CB/000?text=PC+Case"], rating=4.6, reviews=500, 
        features=[
            "Dual-chamber design for clean cable management.",
            "Reversible chassis for a left or right-side view.",
            "Supports up to a 420mm radiator and 10 fans.",
            "Flexible GPU mounting options (horizontal, vertical, or upright).",
            "Tool-less clip-in panels for easy access."
        ],
        specs={
            "Brand": "Lian Li", "Model": "O11 Dynamic EVO", "Form Factor": "Mid-Tower", "Material": "Aluminum, Tempered Glass, Steel", 
            "Motherboard Support": "E-ATX, ATX, Micro-ATX, Mini-ITX"
        }
    ),
    Product("NZXT Kraken Z73 AIO Cooler", 279.00, "A 360mm all-in-one liquid CPU cooler with a customizable LCD display, a 7th-gen Asetek pump, and high-performance fans for optimal cooling.", "Gaming Components", ["https://placehold.co/600x400/FF69B4/FFF?text=AIO+Cooler"], rating=4.8, reviews=600, 
        features=[
            "2.36-inch customizable LCD display for real-time system stats or animated GIFs.",
            "7th-generation Asetek pump for improved flow and reliability.",
            "Three 120mm Aer P120 fans for powerful cooling.",
            "Reinforced tubing with fine nylon mesh sleeves for leak protection.",
            "Broad compatibility with Intel and AMD sockets."
        ],
        specs={
            "Brand": "NZXT", "Model": "Kraken Z73", "Type": "AIO Liquid Cooler", "Radiator Size": "360mm", 
            "Pump Speed": "800 - 2,800 RPM", "Fan Speed": "500 - 2,000 RPM"
        }
    ),
    Product("Arctic P12 PWM PST Fans (5-pack)", 39.99, "A 5-pack of 120mm pressure-optimized fans with PWM Sharing Technology (PST) for synchronized speed control and efficient, quiet cooling.", "Gaming Components", ["https://placehold.co/600x400/87CEEB/FFF?text=Case+Fans"], rating=4.5, reviews=900, 
        features=[
            "PWM Sharing Technology (PST) for synchronized fan speed.",
            "Optimized for static pressure, ideal for heatsinks and radiators.",
            "0 dB mode for silent operation at low loads.",
            "Fluid Dynamic Bearing for quiet operation and extended lifespan.",
            "5-blade impeller for focused airflow."
        ],
        specs={
            "Brand": "Arctic", "Model": "P12 PWM PST", "Size": "120mm", "Quantity": "5-pack", 
            "Fan Speed": "200 - 1800 RPM", "Airflow": "56.30 CFM"
        }
    ),

    # --- Gaming Peripherals (more products) ---
    Product("Alienware AW2725DF OLED Monitor", 899.00, "A 27-inch QD-OLED gaming monitor with a 360Hz refresh rate and 0.03ms response time, designed for competitive gamers who demand the best in speed and visual fidelity.", "Gaming Peripherals", ["https://placehold.co/600x400/1E90FF/FFF?text=Gaming+Monitor"], rating=4.8, reviews=600, 
        features=[
            "27-inch QHD (2560x1440) QD-OLED panel for stunning visuals and true blacks.",
            "360Hz native refresh rate for incredibly smooth gameplay.",
            "0.03ms gray-to-gray response time for virtually no ghosting.",
            "AMD FreeSync™ Premium Pro and VESA AdaptiveSync for tear-free gaming.",
            "VESA HDR TrueBlack 400-certified for incredible color and contrast."
        ],
        specs={
            "Brand": "Alienware", "Model": "AW2725DF", "Screen Size": "27 inches", "Refresh Rate": "360Hz", 
            "Panel Type": "QD-OLED", "Resolution": "2560x1440"
        }
    ),
    Product("Razer BlackWidow V4 Keyboard", 199.99, "A mechanical gaming keyboard with Razer's iconic green switches, per-key RGB lighting, and a host of features designed for gamers and enthusiasts.", "Gaming Peripherals", ["https://placehold.co/600x400/000080/FFF?text=Razer+Keyboard"], rating=4.6, reviews=1800, 
        features=[
            "Razer™ Green Mechanical Switches for a clicky, tactile feel.",
            "Per-key Razer Chroma™ RGB lighting with side underglow.",
            "Detachable, magnetic plush leatherette wrist rest for comfort.",
            "Up to 8000Hz polling rate for near-instantaneous response.",
            "Durable aluminum alloy top plate."
        ],
        specs={
            "Brand": "Razer", "Model": "BlackWidow V4", "Switch Type": "Razer Green Mechanical", "Layout": "Full-size", 
            "Connectivity": "Wired (USB-C)", "RGB": "Razer Chroma™ RGB"
        }
    ),
    Product("Logitech G502 X PLUS Mouse", 159.99, "A wireless RGB gaming mouse with the iconic G502 shape, featuring LIGHTFORCE hybrid optical-mechanical switches and the HERO 25K sensor for ultimate performance.", "Gaming Peripherals", ["https://placehold.co/600x400/0000FF/FFF?text=Logitech+Mouse"], rating=4.7, reviews=4500, 
        features=[
            "LIGHTFORCE hybrid optical-mechanical switches for speed and reliability.",
            "HERO 25K optical sensor with sub-micron accuracy.",
            "LIGHTSPEED wireless technology for a faster response rate.",
            "13 programmable controls and a dual-mode scroll wheel.",
            "LIGHTSYNC RGB with 8-zone lighting and active play detection."
        ],
        specs={
            "Brand": "Logitech", "Model": "G502 X PLUS", "Connectivity": "Wireless (LIGHTSPEED)", "Sensor": "HERO 25K", 
            "DPI": "100 - 25,600", "Weight": "106g"
        }
    ),
    Product("SteelSeries QcK Heavy Mousepad", 29.99, "An extra-thick gaming mousepad with a micro-woven cloth surface, designed for comfort, precision, and stability during intense gaming sessions.", "Gaming Peripherals", ["https://placehold.co/600x400/8A2BE2/FFF?text=Mousepad"], rating=4.7, reviews=2100, 
        features=[
            "Extra-thick rubber base for a solid gaming platform and wrist comfort.",
            "High thread count, micro-woven cloth surface for precise mouse tracking.",
            "Non-slip rubber base to prevent unwanted movement.",
            "Optimized for both low and high CPI/DPI tracking movements.",
            "Durable and washable for easy cleaning."
        ],
        specs={
            "Brand": "SteelSeries", "Model": "QcK Heavy", "Material": "Micro-woven cloth, Rubber base", "Size": "Large (450mm x 400mm)", 
            "Thickness": "6mm"
        }
    ),
    Product("HyperX Cloud II Headset", 99.99, "A legendary gaming headset known for its comfort, audio quality, and durability, featuring virtual 7.1 surround sound and a detachable noise-canceling microphone.", "Gaming Peripherals", ["https://placehold.co/600x400/4B0082/FFF?text=Gaming+Headset"], rating=4.5, reviews=50000, 
        features=[
            "Hardware-driven virtual 7.1 surround sound.",
            "53mm dynamic drivers with neodymium magnets for superior audio.",
            "Detachable, noise-canceling microphone.",
            "100% memory foam on the headband and leatherette cushions.",
            "Durable aluminum frame."
        ],
        specs={
            "Brand": "HyperX", "Model": "Cloud II", "Connectivity": "Wired (USB, 3.5mm)", "Audio": "Virtual 7.1 Surround Sound", 
            "Driver": "53mm dynamic", "Microphone": "Detachable, noise-canceling"
        }
    ),
    Product("Blue Yeti USB Microphone", 129.99, "A versatile USB microphone with multiple polar patterns, perfect for podcasting, streaming, music recording, and voice-overs.", "Gaming Peripherals", ["https://placehold.co/600x400/9400D3/FFF?text=USB+Mic"], rating=4.6, reviews=3200, 
        features=[
            "Four selectable polar patterns: Cardioid, Omnidirectional, Bidirectional, and Stereo.",
            "On-board controls for headphone volume, pattern selection, instant mute, and microphone gain.",
            "3.5mm headphone jack with zero-latency monitoring.",
            "Plug-and-play USB connectivity for Windows and macOS.",
            "Innovative design with an adjustable desktop stand."
        ],
        specs={
            "Brand": "Blue", "Model": "Yeti", "Connectivity": "USB", "Polar Patterns": "Cardioid, Bidirectional, Omnidirectional, Stereo", 
            "Sample Rate": "48 kHz", "Bit Rate": "16-bit"
        }
    ),

    # --- Gaming Furniture (more products) ---
    Product("Secretlab TITAN Evo Gaming Chair", 529.00, "An ergonomic gaming chair with a 4-way lumbar support system, magnetic memory foam head pillow, and a pebble seat base for ultimate comfort and support during long gaming sessions.", "Gaming Furniture", ["https://placehold.co/600x400/B22222/FFF?text=Gaming+Chair"], rating=4.8, reviews=12000, 
        features=[
            "4-way L-ADAPT™ Lumbar Support System for personalized ergonomic support.",
            "Magnetic Memory Foam Head Pillow for easy adjustments and cooling comfort.",
            "Full-metal 4D armrests with CloudSwap™ replacement system.",
            "Up to 165° of recline for various gaming and relaxation positions.",
            "Available in multiple upholstery options, including SoftWeave™ Plus fabric and NEO™ Hybrid Leatherette."
        ],
        specs={
            "Brand": "Secretlab", "Model": "TITAN Evo", "Material": "Varies by selection", "Recline": "165 degrees", 
            "Lumbar Support": "4-way L-ADAPT™", "Warranty": "Up to 5 years"
        }
    ),
    Product("FlexiSpot Gaming Desk", 299.00, "A height-adjustable gaming desk with a spacious, gaming-optimized desktop surface, robust build quality, and excellent cable management for a clean and ergonomic setup.", "Gaming Furniture", ["https://placehold.co/600x400/8B0000/FFF?text=Gaming+Desk"], rating=4.7, reviews=1900, 
        features=[
            "Electric height adjustment with programmable presets.",
            "Gaming-optimized desktop surface that doubles as a mouse pad.",
            "Powerful dual motors with a weight capacity of up to 440 lbs.",
            "Integrated cable management system for a clutter-free workspace.",
            "Ergonomic design with curved edges for wrist comfort."
        ],
        specs={
            "Brand": "FlexiSpot", "Type": "Standing Desk", "Material": "Steel, Particle Board", "Weight Capacity": "Up to 440 lbs", 
            "Height Adjustment": "Electric", "Desktop Size": "Varies by model"
        }
    ),
    Product("Respawn RSP-900 Racing Style Gaming Recliner", 319.99, "A comfortable reclining chair designed for console gamers, featuring a continuous surface with independent controls for the back and footrest, a cup holder, and a removable side pouch.", "Gaming Furniture", ["https://placehold.co/600x400/8B0000/FFF?text=Gaming+Recliner"], rating=4.4, reviews=950, 
        features=[
            "Reclines up to 135 degrees with an independently operated footrest.",
            "Integrated cup holder in the left arm and a removable side pouch for controllers.",
            "360-degree swivel base for easy maneuvering.",
            "Segmented padding and a plush, removable headrest pillow for comfort.",
            "Durable construction with a 275 lbs weight capacity."
        ],
        specs={
            "Brand": "Respawn", "Model": "RSP-900", "Material": "Fabric or Bonded Leather", "Recline": "Up to 135 degrees", 
            "Weight Capacity": "275 lbs", "Features": "Cup holder, Side pouch"
        }
    ),

    # --- Home Decor (more products) ---
    Product("Abstract Canvas Wall Art", 79.99, "A modern and versatile piece of abstract canvas wall art that can dynamically transform a room by introducing vibrant colors, intriguing shapes, and rich textures.", "Home Decor", ["https://placehold.co/600x400/3A4F6A/FFF?text=Wall+Art"], rating=4.5, reviews=350, 
        features=[
            "Vibrant colors and intriguing shapes to create a focal point in any room.",
            "Available in multiple sizes to fit any wall space.",
            "Printed on high-quality canvas for a gallery-style aesthetic.",
            "Ready to hang with pre-installed hardware.",
            "Versatile design that complements various interior styles."
        ],
        specs={
            "Type": "Canvas Print", "Theme": "Abstract", "Material": "Canvas", "Frame": "Unframed", 
            "Sizes": "Small, Medium, Large"
        }
    ),
    Product("Velvet Throw Pillow (Set of 2)", 24.99, "A set of two plush and luxurious velvet throw pillows that add a touch of color, texture, and comfort to any living space.", "Home Decor", ["https://placehold.co/600x400/7E57C2/FFF?text=Throw+Pillow"], rating=4.7, reviews=1250, 
        features=[
            "Set of two pillows with soft and luxurious velvet covers.",
            "Filled with plush polyester fiberfill for ultimate comfort.",
            "Hidden zipper for a seamless look and easy cover removal.",
            "Available in a wide variety of colors to match any decor.",
            "Machine washable covers for easy care."
        ],
        specs={
            "Material": "Velvet (100% Polyester)", "Quantity": "Set of 2", "Size": "18x18 inches", "Closure": "Hidden Zipper", 
            "Care": "Machine Washable"
        }
    ),
    Product("Chunky Knit Throw Blanket", 49.99, "A warm, cozy, and stylish chunky knit throw blanket that adds a touch of texture and dimension to your home decor. Perfect for layering on a bed or sofa.", "Home Decor", ["https://placehold.co/600x400/C5CAE9/000?text=Throw+Blanket"], rating=4.8, reviews=2100, 
        features=[
            "Made from soft and durable acrylic or chenille yarn.",
            "Hand-knitted with large, open-weave stitches for a distinctive look.",
            "Breathable and moisture-wicking for year-round comfort.",
            "Available in multiple sizes and colors.",
            "Adds a touch of modern style to any room."
        ],
        specs={
            "Material": "Acrylic or Chenille", "Size": "Varies by selection", "Weave": "Chunky Knit", "Care": "Varies by material", 
            "Style": "Modern, Cozy"
        }
    ),

    # --- Furniture (more products) ---
    Product("Minimalist Coffee Table", 149.00, "A sleek and functional coffee table with a minimalist design, perfect for modern living rooms. It features clean lines and a durable MDF construction.", "Furniture", ["https://placehold.co/600x400/424242/FFF?text=Coffee+Table"], rating=4.3, reviews=800, 
        features=[
            "Clean lines and a simple, geometric shape for a minimalist aesthetic.",
            "Made from durable MDF for long-lasting use.",
            "Easy to assemble and maintain.",
            "Available in a variety of neutral tones to complement any decor.",
            "Includes a lower shelf for additional storage."
        ],
        specs={
            "Material": "MDF", "Style": "Minimalist", "Shape": "Rectangular", "Dimensions": "Varies by model", 
            "Assembly Required": "Yes"
        }
    ),
    Product("Storage Ottoman with Lid", 79.00, "A versatile and stylish storage ottoman with a lid, perfect for adding extra seating and concealed storage to any room. It features a durable frame and a comfortable, padded seat.", "Furniture", ["https://placehold.co/600x400/212121/FFF?text=Storage+Ottoman"], rating=4.6, reviews=1500, 
        features=[
            "Hidden storage compartment for blankets, pillows, and other items.",
            "Can be used as extra seating, a footrest, or a coffee table.",
            "Upholstered in a variety of fabrics, including linen and velvet.",
            "Sturdy construction with a solid wood or MDF frame.",
            "Available in multiple shapes, sizes, and colors."
        ],
        specs={
            "Material": "Varies by selection", "Function": "Storage, Seating", "Shape": "Varies by model", 
            "Lid Type": "Flip-top or Removable", "Weight Capacity": "Varies by model"
        }
    ),

    # --- Kitchenware (more products) ---
    Product("High-Speed Blender", 120.00, "A powerful high-speed blender with a 1200-watt motor, perfect for making smoothies, soups, and grinding tough ingredients. It features multiple speed settings and a large, dishwasher-safe jar.", "Kitchenware", ["https://placehold.co/600x400/EF4444/FFF?text=Blender"], rating=4.7, reviews=3500, 
        features=[
            "Powerful 1200-watt motor for pulverizing ingredients.",
            "Variable speed control and preset programs for smoothies, soups, and more.",
            "Large, 64-ounce BPA-free Tritan container.",
            "Hardened stainless steel blades for durability and efficient blending.",
            "Self-cleaning function for easy cleanup."
        ],
        specs={
            "Brand": "Generic", "Power": "1200W", "Capacity": "64 oz", "Material": "BPA-Free Tritan", 
            "Speeds": "Variable", "Dishwasher Safe": "Yes (Jar)"
        }
    ),
    Product("Non-Stick Cookware Set (5-piece)", 150.00, "An essential 5-piece non-stick cookware set with a durable aluminum core for fast, even heating. The set includes a fry pan, a saucepan with a lid, and a sauté pan with a lid.", "Kitchenware", ["https://placehold.co/600x400/FFDDC1/000?text=Cookware"], rating=4.5, reviews=2800, 
        features=[
            "Durable, non-stick interior for easy food release and cleanup.",
            "Aluminum core for fast and even heat distribution.",
            "Ergonomic, stay-cool handles for a secure grip.",
            "Tempered glass lids to monitor cooking without releasing heat.",
            "Oven safe up to 350°F and compatible with all cooktops, including induction."
        ],
        specs={
            "Material": "Aluminum, Stainless Steel Base", "Coating": "Non-Stick (PFOA-Free)", "Pieces": "5", 
            "Oven Safe": "Up to 350°F", "Induction Compatible": "Yes"
        }
    ),
    Product("Stainless Steel Cutlery Set (4-person)", 45.00, "A durable and elegant 16-piece stainless steel cutlery set for four people, perfect for everyday use and special occasions. The set includes dinner knives, dinner forks, salad forks, and teaspoons.", "Kitchenware", ["https://placehold.co/600x400/A0A0A0/FFF?text=Cutlery+Set"], rating=4.6, reviews=1200, 
        features=[
            "16-piece set includes service for four.",
            "Made from high-quality 18/10 stainless steel for durability and rust resistance.",
            "Modern, ergonomic design with a mirror polish finish.",
            "Dishwasher safe for easy cleanup.",
            "Well-balanced with a comfortable weight and smooth body curves."
        ],
        specs={
            "Material": "18/10 Stainless Steel", "Quantity": "16 pieces (Service for 4)", "Finish": "Mirror Polish", 
            "Dishwasher Safe": "Yes", "Style": "Modern"
        }
    ),

    # --- Beauty & Personal Care (more products) ---
    Product("Hydrating Face Cream SPF 30", 35.00, "A daily hydrating face cream with broad-spectrum SPF 30 to protect and nourish your skin. This lightweight, non-greasy formula is perfect for all skin types.", "Beauty & Personal Care", ["https://placehold.co/600x400/F472B6/FFF?text=Face+Cream"], rating=4.6, reviews=4800, 
        features=[
            "Broad-spectrum SPF 30 protection against UVA and UVB rays.",
            "Infused with Hyaluronic Acid to lock in moisture and keep skin supple.",
            "Non-comedogenic formula that won't clog pores.",
            "Lightweight and non-greasy, perfect for daily use under makeup.",
            "Helps to restore and strengthen the skin's natural barrier."
        ],
        specs={
            "Type": "Face Cream", "Volume": "50ml", "SPF": "30", "Key Ingredients": "Hyaluronic Acid, Niacinamide", 
            "Skin Type": "All", "Fragrance-Free": "Yes"
        }
    ),
    Product("Argan Oil Hair Serum", 22.00, "A nourishing hair serum infused with argan oil to add shine, reduce frizz, and protect hair from heat damage. Suitable for all hair types.", "Beauty & Personal Care", ["https://placehold.co/600x400/DAA520/FFF?text=Hair+Serum"], rating=4.7, reviews=5200, 
        features=[
            "Infused with pure Argan Oil for deep hydration and moisture.",
            "Tames flyaways, eliminates frizz, and promotes a smoother hair texture.",
            "Provides a protective barrier against heat styling and UV damage.",
            "Lightweight, non-greasy formula that absorbs quickly.",
            "Free from sulfates, phosphates, and parabens."
        ],
        specs={
            "Type": "Hair Serum", "Volume": "100ml", "Key Ingredient": "Argan Oil", "Hair Type": "All", 
            "Benefits": "Frizz control, Shine, Heat protection"
        }
    ),

    # --- Makeup & Beauty (more products) ---
    Product("Primer to smooth skin", 18.00, "A smoothing primer that creates an even, refined surface for makeup application, blurring imperfections and extending makeup wear.", "Makeup & Beauty", ["https://placehold.co/600x400/FFCCCC/000?text=Primer"], rating=4.5, reviews=1100, 
        features=[
            "Blurs fine lines and minimizes the appearance of pores.",
            "Creates a smooth canvas for seamless makeup application.",
            "Extends the life of your makeup, even in varying weather conditions.",
            "Formulated with skin-enhancing ingredients like silicones and hyaluronic acid.",
            "Can be worn alone for a naturally polished look."
        ],
        specs={
            "Product Type": "Primer", "Finish": "Matte", "Skin Type": "All", "Benefit": "Smoothing", 
            "Key Ingredients": "Silicones, Hyaluronic Acid"
        }
    ),
    Product("Foundation Liquid", 25.00, "A versatile liquid foundation that provides buildable coverage to even out skin tone and conceal imperfections, leaving a natural-looking finish.", "Makeup & Beauty", ["https://placehold.co/600x400/FFDDCC/000?text=Foundation"], rating=4.4, reviews=1500, 
        features=[
            "Buildable coverage from sheer to full.",
            "Blends seamlessly with the skin for a natural look.",
            "Available in a wide range of shades to match any skin tone.",
            "Formulated for different skin types, including oily, dry, and sensitive.",
            "Many formulas include moisturizing ingredients and SPF."
        ],
        specs={
            "Product Type": "Foundation", "Coverage": "Buildable", "Finish": "Natural, Matte, or Dewy", "Skin Type": "All", 
            "Key Ingredients": "Varies by formula"
        }
    ),
    Product("Neutral Eyeshadow Palette", 28.00, "A versatile eyeshadow palette with a curated selection of neutral shades in matte, shimmer, and metallic finishes, perfect for creating a variety of looks from natural to dramatic.", "Makeup & Beauty", ["https://placehold.co/600x400/CCFFFF/000?text=Eyeshadow"], rating=4.7, reviews=1200, 
        features=[
            "A mix of matte, shimmer, and metallic finishes.",
            "Highly pigmented shades for single-swipe color payoff.",
            "Smooth, buttery texture that is easy to blend.",
            "Long-lasting, crease-proof wear.",
            "Compact and sleek packaging, perfect for travel."
        ],
        specs={
            "Product Type": "Eyeshadow Palette", "Shades": "Varies by palette", "Finishes": "Matte, Shimmer, Metallic", 
            "Pigmentation": "High", "Blendability": "Easy"
        }
    ),
    Product("Volumizing Mascara", 13.00, "A volumizing mascara that creates fuller, thicker, and more dramatic-looking eyelashes with a specially designed brush that coats each lash from root to tip.", "Makeup & Beauty", ["https://placehold.co/600x400/CCDDFF/000?text=Mascara"], rating=4.6, reviews=1800, 
        features=[
            "XXL or large brush to maximize volume.",
            "Formulated with waxes and other volumizing ingredients.",
            "Smudge-proof, water-resistant, and long-lasting wear.",
            "Often includes conditioning ingredients like panthenol or Vitamin E.",
            "Available in clean, cruelty-free, and vegan formulas."
        ],
        specs={
            "Product Type": "Mascara", "Color": "Black", "Benefit": "Volumizing", "Brush Type": "Varies by product", 
            "Key Ingredients": "Waxes, Conditioning Agents"
        }
    ),
    
    # --- Fashion (more products) ---
    Product("Classic Denim Jacket", 75.00, "A timeless and versatile denim jacket made from 100% cotton, featuring a classic fit, button-front closure, and chest pockets. A must-have for any wardrobe.", "Fashion", ["https://placehold.co/600x400/3B82F6/FFF?text=Denim+Jacket"], rating=4.5, reviews=1800, 
        features=[
            "Made from 100% cotton denim for durability and comfort.",
            "Classic fit with a button-front closure and chest pockets.",
            "Versatile design that can be dressed up or down.",
            "Develops a unique patina over time.",
            "Available in a variety of washes."
        ],
        specs={
            "Material": "100% Cotton Denim", "Fit": "Classic", "Closure": "Button-front", "Pockets": "Chest and side pockets", 
            "Care": "Machine wash cold"
        }
    ),
    Product("Linen Summer Dress", 55.00, "A light and breezy linen summer dress, perfect for warm weather. This dress is made from breathable linen fabric and features a relaxed fit for all-day comfort.", "Fashion", ["https://placehold.co/600x400/10B981/FFF?text=Summer+Dress"], rating=4.4, reviews=950, 
        features=[
            "Made from breathable and moisture-wicking linen fabric.",
            "Relaxed fit for a comfortable and airy feel.",
            "Available in a variety of summer-ready colors and patterns.",
            "Versatile design that can be dressed up or down.",
            "Easy to care for and becomes softer with each wash."
        ],
        specs={
            "Material": "Linen", "Style": "Casual Dress", "Fit": "Relaxed", "Length": "Varies by style", 
            "Care": "Machine wash cold or hand wash"
        }
    ),
    Product("Leather Ankle Boots", 120.00, "Stylish and durable leather ankle boots that are perfect for any occasion. These boots are crafted from high-quality genuine leather and feature a comfortable, cushioned insole.", "Fashion", ["https://placehold.co/600x400/A52A2A/FFF?text=Boots"], rating=4.6, reviews=1300, 
        features=[
            "Crafted from high-quality genuine leather for durability and style.",
            "Cushioned insole for all-day comfort.",
            "Versatile design that pairs well with jeans, skirts, and dresses.",
            "Side zipper closure for easy on and off.",
            "Available in a variety of colors and finishes."
        ],
        specs={
            "Material": "Genuine Leather", "Heel Type": "Varies by style", "Closure": "Side Zipper", "Toe Shape": "Varies by style", 
            "Occasion": "Casual, Formal"
        }
    ),
    Product("Cashmere Scarf", 90.00, "An ultra-soft and luxurious cashmere scarf that provides exceptional warmth without the bulk. Made from 100% pure Grade A cashmere.", "Fashion", ["https://placehold.co/600x400/9CA3AF/FFF?text=Scarf"], rating=4.8, reviews=750, 
        features=[
            "Made from 100% pure Grade A cashmere for superior softness and warmth.",
            "Lightweight and breathable for versatile, all-season wear.",
            "Available in a wide range of colors and patterns.",
            "Features a classic fringe detail.",
            "A luxurious and timeless accessory."
        ],
        specs={
            "Material": "100% Cashmere", "Dimensions": "Varies by style", "Ply": "2-ply", "Origin": "Mongolia, China, Himalayas", 
            "Care": "Dry clean or hand wash"
        }
    ),
    Product("Men's Slim-Fit Chinos", 45.00, "Comfortable and stylish slim-fit chinos that offer a modern, tailored look. Made from a stretch cotton fabric for all-day comfort and flexibility.", "Fashion", ["https://placehold.co/600x400/F5DEB3/000?text=Chinos"], rating=4.3, reviews=2200, 
        features=[
            "Slim-fit design for a modern, tailored silhouette.",
            "Made from a stretch cotton blend for comfort and flexibility.",
            "Versatile design that can be dressed up or down.",
            "Classic four-pocket styling.",
            "Available in a variety of colors."
        ],
        specs={
            "Material": "Cotton Blend (with Elastane/Spandex)", "Fit": "Slim-Fit", "Style": "Chinos", "Pockets": "4", 
            "Care": "Machine wash"
        }
    ),
    Product("Leather Belt", 35.00, "A classic leather belt made from high-quality full-grain leather, perfect for completing any outfit. This durable belt will develop a unique patina over time.", "Fashion", ["https://placehold.co/600x400/8B4513/FFF?text=Leather+Belt"], rating=4.5, reviews=3100, 
        features=[
            "Made from high-quality full-grain leather for durability.",
            "Develops a unique patina over time.",
            "Classic and versatile design with a durable metal buckle.",
            "Available in a variety of colors and widths.",
            "Perfect for both casual and formal wear."
        ],
        specs={
            "Material": "Full-Grain Leather", "Width": "Varies by style", "Buckle": "Metal", "Style": "Casual, Dress", 
            "Care": "Wipe clean"
        }
    ),

    # --- Women's Clothing ---
    Product("Women's Button-up Shirt", 35.00, "A versatile and timeless button-up shirt, perfect for any occasion. Made from 100% cotton, it offers a classic fit and is available in a variety of colors.", "Women's Clothing", ["https://placehold.co/600x400/F0F0F0/000?text=Women's+Shirt"], rating=4.6, reviews=1500, 
        features=[
            "Made from 100% breathable cotton for all-day comfort.",
            "Classic fit that can be dressed up or down.",
            "Features a button-front closure and a single chest pocket.",
            "Available in a wide range of colors and patterns.",
            "Easy to care for and machine washable."
        ],
        specs={
            "Material": "100% Cotton", "Style": "Button-up", "Fit": "Classic", "Sleeves": "Long Sleeve", 
            "Care": "Machine wash cold"
        }
    ),
    Product("Women's Straight-leg Jeans", 45.00, "Classic straight-leg jeans that offer a flattering and comfortable fit. Made from a durable denim with a hint of stretch for all-day comfort.", "Women's Clothing", ["https://placehold.co/600x400/C0C0C0/000?text=Women's+Jeans"], rating=4.5, reviews=2200, 
        features=[
            "Classic straight-leg fit from hip to ankle.",
            "Made from a blend of cotton, polyester, and spandex for stretch and recovery.",
            "Mid-rise waist for a comfortable and flattering fit.",
            "Classic five-pocket styling.",
            "Available in a variety of washes."
        ],
        specs={
            "Material": "Cotton Blend", "Fit": "Straight-leg", "Rise": "Mid-rise", "Style": "5-pocket", 
            "Care": "Machine wash cold"
        }
    ),
    Product("Women's Little Black Dress", 60.00, "The essential little black dress, a versatile and timeless piece for any wardrobe. This dress can be dressed up or down for any occasion.", "Women's Clothing", ["https://placehold.co/600x400/808080/FFF?text=Little+Black+Dress"], rating=4.7, reviews=1800, 
        features=[
            "Classic and versatile design for any occasion.",
            "Made from a comfortable and flattering fabric with a hint of stretch.",
            "Available in a variety of styles, including A-line, sheath, and wrap.",
            "Can be easily dressed up or down with accessories.",
            "A timeless wardrobe essential."
        ],
        specs={
            "Color": "Black", "Style": "Varies by selection", "Material": "Varies by style", "Length": "Varies by style", 
            "Occasion": "Casual, Formal, Party"
        }
    ),

    # --- Men's Clothing ---
    Product("Men's Classic White T-shirt", 18.00, "A versatile and timeless wardrobe staple, this classic white T-shirt is made from 100% combed ringspun cotton for a soft, comfortable feel.", "Men's Clothing", ["https://placehold.co/600x400/F0F0F0/000?text=Men's+T-shirt"], rating=4.7, reviews=3000, 
        features=[
            "Made from 100% combed ringspun cotton for softness and breathability.",
            "Classic crew neck and short sleeves for a timeless look.",
            "Available in a variety of fits, from slim to relaxed.",
            "Durable construction with reinforced shoulder seams and double-needle hems.",
            "Pre-shrunk to minimize shrinkage after washing."
        ],
        specs={
            "Material": "100% Cotton", "Color": "White", "Fit": "Varies by selection", "Neckline": "Crew Neck", 
            "Care": "Machine wash cold"
        }
    ),
    Product("Men's Go-to Jeans", 50.00, "A comfortable and durable pair of go-to jeans, perfect for everyday wear. These jeans are made from a stretch denim fabric for all-day comfort and flexibility.", "Men's Clothing", ["https://placehold.co/600x400/A9A9A9/FFF?text=Men's+Jeans"], rating=4.5, reviews=2500, 
        features=[
            "Made from a blend of cotton and elastane for stretch and comfort.",
            "Classic five-pocket styling.",
            "Available in a variety of fits, including slim, straight, and relaxed.",
            "Durable construction with reinforced stitching.",
            "Available in a range of washes."
        ],
        specs={
            "Material": "Cotton Blend (with Elastane)", "Fit": "Varies by selection", "Style": "5-pocket", "Rise": "Mid-rise", 
            "Care": "Machine wash cold"
        }
    ),
    Product("Men's Navy Blazer", 85.00, "A versatile and timeless navy blazer that can be dressed up or down for any occasion. Made from a high-quality wool blend, it features a classic notch lapel and two-button closure.", "Men's Clothing", ["https://placehold.co/600x400/4682B4/FFF?text=Navy+Blazer"], rating=4.6, reviews=1100, 
        features=[
            "Made from a high-quality wool blend for a luxurious feel and drape.",
            "Classic notch lapel and two-button closure.",
            "Versatile design that can be paired with dress pants, chinos, or jeans.",
            "Available in a variety of fits, from slim to classic.",
            "Features patch pockets and a double vent for a classic look."
        ],
        specs={
            "Material": "Wool Blend", "Style": "Blazer", "Fit": "Varies by selection", "Lapel": "Notch", 
            "Closure": "Two-button"
        }
    ),

    # --- Baby Clothing ---
    Product("Baby Onesies (5-pack)", 25.00, "A pack of five soft and comfortable baby onesies, perfect for everyday wear. Made from 100% cotton, these onesies are gentle on your baby's delicate skin.", "Baby Clothing", ["https://placehold.co/600x400/FFD1DC/000?text=Baby+Onesies"], rating=4.8, reviews=4500, 
        features=[
            "Made from 100% soft, breathable cotton.",
            "Expandable lap shoulder neckline for easy dressing.",
            "Nickel-free snaps on a reinforced panel for quick and easy diaper changes.",
            "Tagless design to prevent irritation.",
            "Machine washable and dryable for easy care."
        ],
        specs={
            "Material": "100% Cotton", "Quantity": "5-pack", "Sleeves": "Short or Long Sleeve", "Closure": "Snap", 
            "Care": "Machine washable"
        }
    ),
    Product("Baby Sleepsuit", 18.00, "A cozy and comfortable one-piece sleepsuit for your baby, designed for both sleep and play. Made from soft, breathable fabric to keep your baby comfortable all night long.", "Baby Clothing", ["https://placehold.co/600x400/ADD8E6/000?text=Baby+Sleepsuit"], rating=4.7, reviews=3200, 
        features=[
            "Made from soft and breathable fabric, such as cotton or bamboo.",
            "Full-length zipper or snaps for easy diaper changes.",
            "Footed design to keep your baby's feet warm.",
            "Fold-over cuffs to prevent scratching (on smaller sizes).",
            "Available in a variety of cute prints and colors."
        ],
        specs={
            "Material": "Varies by style (Cotton, Bamboo, etc.)", "Style": "Sleepsuit/Babygrow", "Closure": "Zipper or Snaps", 
            "Footed": "Yes (or with foldable cuffs)", "Care": "Machine washable"
        }
    ),

    # --- Kids & Teens Clothing ---
    Product(
        "Kids' Graphic T-shirt", 15.00, "Fun and comfortable graphic t-shirt for kids, perfect for school and casual wear. Made from soft, breathable cotton.", "Kids & Teens Clothing",
        ["https://placehold.co/600x400/87CEEB/FFF?text=Kids+T-shirt"],
        rating=4.4, reviews=1800,
        features=["Fun and colorful graphics", "Made from 100% soft cotton", "Comfortable crew neck", "Durable and machine washable"],
        specs={"Material": "100% Cotton", "Sleeve Type": "Short Sleeve", "Fit": "Regular", "Care": "Machine Wash"}
    ),
    Product(
        "Teens' Hoodie Fleece", 40.00, "A warm and stylish fleece hoodie for teens, perfect for layering in cooler weather. Features a soft fleece lining and a kangaroo pocket.", "Kids & Teens Clothing",
        ["https://placehold.co/600x400/4682B4/FFF?text=Teens+Hoodie"],
        rating=4.6, reviews=900,
        features=["Warm and soft fleece lining", "Kangaroo pocket for essentials", "Adjustable drawstring hood", "Ribbed cuffs and hem for a snug fit"],
        specs={"Material": "Cotton-Poly Fleece Blend", "Fit": "Regular", "Pockets": "Kangaroo Pocket", "Care": "Machine Wash"}
    ),

    # --- Senior Clothing ---
    Product(
        "Senior Easy-On Knit Top", 40.00, "A comfortable and stylish easy-on knit top for seniors, designed for ease of dressing. This top features a soft, breathable fabric and a loose fit for all-day comfort. The open-back design with snap closures allows for dressing with minimal effort, making it ideal for those with limited mobility.", "Senior Clothing",
        ["https://placehold.co/600x400/E6E6FA/000?text=Senior+Top"],
        rating=4.7, reviews=600,
        features=["Open-back design with snap closures for easy dressing", "Soft, breathable, and stretchable knit fabric", "Loose and comfortable fit", "Designed to prevent pressure points", "Stylish design with full coverage"],
        specs={"Material": "Polyester Blend", "Closure": "Snaps", "Sleeves": "Three-Quarter Length", "Care": "Machine Washable"}
    ),
    Product(
        "Senior Supportive Shoes", 70.00, "Orthopedic supportive shoes designed to provide exceptional comfort, stability, and safety for seniors. These shoes feature a non-slip sole, excellent arch support, and a roomy toe box to accommodate various foot conditions. The easy-to-use closures make them simple to put on and take off.", "Senior Clothing",
        ["https://placehold.co/600x400/BA55D3/FFF?text=Supportive+Shoes"],
        rating=4.8, reviews=800,
        features=["Non-slip, high-traction rubber sole to reduce fall risk", "Excellent arch support for even weight distribution", "Wide toe box to prevent crowding and irritation", "Cushioned insole for shock absorption", "Easy-to-manage Velcro or elastic lace closures", "Breathable materials to keep feet dry"],
        specs={"Type": "Orthopedic/Supportive", "Closure": "Velcro/Elastic Laces", "Sole": "Non-Slip Rubber", "Insole": "Cushioned Memory Foam", "Upper Material": "Breathable Mesh/Leather"}
    ),

    # --- Footwear ---
    Product(
        "Men's Running Shoes", 80.00, "High-performance running shoes designed for both comfort and speed. Featuring a lightweight and breathable mesh upper, a responsive cushioned midsole for excellent energy return, and a durable rubber outsole for superior traction. Perfect for road running and daily training.", "Footwear",
        ["https://placehold.co/600x400/4CAF50/FFF?text=Running+Shoes"],
        rating=4.8, reviews=6000,
        features=["Breathable engineered mesh upper for ventilation", "Responsive midsole cushioning for a springy feel", "Durable rubber outsole with high-traction tread", "Padded collar and tongue for added comfort", "Lightweight design for reduced fatigue"],
        specs={"Type": "Road Running", "Upper": "Engineered Mesh", "Midsole": "EVA Foam", "Outsole": "High-Abrasion Rubber", "Heel Drop": "10mm"}
    ),
    Product(
        "Women's Ballet Flats", 40.00, "Classic and versatile ballet flats that blend timeless style with everyday comfort. These slip-on flats are crafted from soft, flexible faux leather and feature a cushioned insole for all-day wear. The minimal, elegant design makes them a perfect choice for both casual and dressy occasions.", "Footwear",
        ["https://placehold.co/600x400/FFC0CB/000?text=Ballet+Flats"],
        rating=4.5, reviews=2100,
        features=["Classic slip-on ballet flat design", "Soft and flexible faux leather upper", "Cushioned insole for enhanced comfort", "Durable and flexible rubber sole", "Timeless and versatile style"],
        specs={"Upper Material": "Faux Leather", "Sole": "Rubber", "Toe Style": "Rounded", "Heel Height": "0.25 inches", "Occasion": "Casual, Dress"}
    ),
    Product(
        "Hiking Boots Waterproof", 110.00, "Durable and waterproof hiking boots built for rugged trails and varied conditions. These boots feature a waterproof membrane to keep your feet dry, an aggressive high-traction outsole for superior grip, and excellent ankle support for stability on uneven terrain.", "Footwear",
        ["https://placehold.co/600x400/795548/FFF?text=Hiking+Boots"],
        rating=4.6, reviews=1500,
        features=["Waterproof yet breathable membrane to keep feet dry", "High-traction rubber outsole with deep lugs for superior grip", "Over-the-ankle design for enhanced support and stability", "Cushioned midsole for shock absorption and comfort", "Protective toe cap to guard against rocks and debris"],
        specs={"Type": "Hiking Boots", "Waterproofing": "Waterproof Membrane", "Upper": "Leather and Mesh", "Outsole": "High-Traction Rubber", "Midsole": "EVA Foam"}
    ),

    # --- Jewellery ---
    Product(
        "Gold Chain Necklace 18K", 250.00, "An elegant and timeless 18K gold chain necklace that offers a rich, vibrant color and a luxurious feel. Composed of 75% pure gold, this chain provides a perfect balance of durability and purity, making it suitable for everyday wear. Its hypoallergenic properties make it an excellent choice for sensitive skin.", "Jewellery",
        ["https://placehold.co/600x400/DAA520/FFF?text=Gold+Chain"],
        rating=4.8, reviews=400,
        features=["Made from 18K gold (75% pure gold) for a rich color and durability", "Hypoallergenic and suitable for sensitive skin", "Secured with a classic lobster claw clasp", "Available in various chain styles and lengths", "A timeless and versatile piece for any occasion"],
        specs={"Material": "18K Gold Plated", "Clasp Type": "Lobster Claw", "Style": "Chain", "Purity": "18 Karat"}
    ),
    Product(
        "Diamond Stud Earrings", 350.00, "A classic pair of sparkling diamond stud earrings, perfect for adding a touch of elegance to any outfit. Each earring features a brilliant-cut diamond held securely in a 4-prong sterling silver setting. These timeless earrings are a must-have for any jewellery collection.", "Jewellery",
        ["https://placehold.co/600x400/BDB76B/000?text=Diamond+Studs"],
        rating=4.9, reviews=200,
        features=["Brilliant-cut diamonds with a total carat weight of 0.5", "Durable and classic sterling silver 4-prong setting", "Secure push-back closures", "Timeless design suitable for everyday wear and special occasions", "Certified conflict-free diamonds"],
        specs={"Total Carat Weight": "0.5 ctw", "Metal": "Sterling Silver", "Setting": "4-Prong", "Backing": "Push Back", "Diamond Cut": "Brilliant"}
    ),

    # --- Cleaning Supplies ---
    Product(
        "Eco-Friendly All-Purpose Cleaner", 12.50, "A powerful and eco-friendly all-purpose cleaner made from natural, plant-based ingredients. This non-toxic formula is safe for your family and pets, and effectively cleans a variety of surfaces without leaving streaks. Packaged in a recyclable bottle, it's a sustainable choice for a clean home.", "Cleaning Supplies",
        ["https://placehold.co/600x400/3B82F6/FFF?text=All-Purpose+Cleaner"],
        rating=4.7, reviews=4200,
        features=["Made with plant-based and biodegradable ingredients", "Free from harsh chemicals like phthalates and phosphates", "Non-toxic and safe for use around kids and pets", "Streak-free formula for a sparkling clean", "Packaged in a recyclable and refillable bottle"],
        specs={"Type": "All-Purpose Cleaner", "Volume": "750ml", "Scent": "Citrus", "Certifications": "EPA Safer Choice, Leaping Bunny"}
    ),
    Product(
        "Cordless Stick Vacuum", 199.00, "A lightweight and powerful cordless stick vacuum designed for versatile and convenient cleaning. With a long-lasting battery and strong suction, it effortlessly cleans all floor types, from hardwood to carpet. It easily converts to a handheld vacuum for cleaning stairs, upholstery, and cars.", "Cleaning Supplies",
        ["https://placehold.co/600x400/A9A9A9/FFF?text=Stick+Vacuum"],
        rating=4.6, reviews=8800,
        features=["Lightweight and portable design for easy maneuverability", "Up to 40 minutes of runtime on a single charge", "Powerful suction for deep cleaning on all floor types", "Converts to a handheld vacuum for versatile cleaning", "HEPA filtration system to trap dust and allergens"],
        specs={"Type": "Cordless Stick Vacuum", "Weight": "5.5 lbs", "Runtime": "Up to 40 minutes", "Filtration": "HEPA", "Attachments": "Crevice tool, Upholstery brush"}
    ),

    # --- Home Storage ---
    Product(
        "Decorative Storage Baskets (Set of 3)", 35.00, "A set of three stylish and functional woven fabric storage baskets, perfect for organizing any room in your home. These versatile baskets are ideal for storing clothes, toys, magazines, and more. The collapsible design allows for easy storage when not in use, and the integrated handles make them easy to carry.", "Home Storage",
        ["https://placehold.co/600x400/FFC0CB/000?text=Storage+Baskets"],
        rating=4.8, reviews=2500,
        features=["Set of three stylish and versatile storage baskets", "Made from durable woven fabric with a wire frame for structure", "Collapsible design for easy storage when not in use", "Integrated handles for convenient carrying", "Perfect for organizing clothes, toys, books, and more"],
        specs={"Material": "Woven Fabric, Wire Frame", "Quantity": "Set of 3", "Sizes": "Small, Medium, Large", "Features": "Collapsible, Integrated Handles"}
    ),

    # --- Bedding ---
    Product(
        "Queen Comforter Set 7-Piece", 89.99, "A luxurious and soft 7-piece queen comforter set, perfect for a restful night's sleep. This comprehensive set includes a plush comforter, matching shams, a bed skirt, and decorative pillows to give your bedroom a coordinated and stylish look. Made from soft, durable microfiber, this set is designed for year-round comfort.", "Bedding",
        ["https://placehold.co/600x400/60A5FA/FFF?text=Comforter+Set"],
        rating=4.5, reviews=9500,
        features=["Complete 7-piece set for a fully dressed bed", "Plush, hypoallergenic microfiber fill for warmth and comfort", "Includes 1 comforter, 2 shams, 1 bed skirt, and 3 decorative pillows", "Elegant design to enhance any bedroom decor", "Machine washable for easy care"],
        specs={"Size": "Queen", "Material": "100% Polyester Microfiber", "Includes": "Comforter, 2 Shams, Bed Skirt, 3 Decorative Pillows", "Fill": "Hypoallergenic Polyester", "Care": "Machine Washable"}
    ),
    Product(
        "Egyptian Cotton Sheet Set Queen", 75.00, "Experience the ultimate in comfort and luxury with this ultra-soft and breathable 400-thread-count Egyptian cotton sheet set. Made from extra-long staple cotton, these sheets are incredibly smooth, durable, and get even softer with every wash. The deep-pocket fitted sheet ensures a secure fit on your mattress.", "Bedding",
        ["https://placehold.co/600x400/ADD8E6/000?text=Cotton+Sheets"],
        rating=4.6, reviews=12500,
        features=["Made from 100% certified extra-long staple Egyptian cotton", "Luxurious 400-thread-count for superior softness and durability", "Breathable and temperature-regulating for year-round comfort", "Deep-pocket fitted sheet fits mattresses up to 18 inches deep", "Set includes 1 flat sheet, 1 fitted sheet, and 2 pillowcases"],
        specs={"Material": "100% Egyptian Cotton", "Thread Count": "400", "Weave": "Sateen", "Size": "Queen", "Includes": "Flat Sheet, Fitted Sheet, 2 Pillowcases"}
    ),

    # --- Office (Existing) ---
    Product(
        "Ergonomic Standing Desk", 349.50, "An adjustable electric standing desk designed to improve posture and boost productivity. With smooth, quiet dual-motor height adjustment and programmable memory presets, you can effortlessly switch between sitting and standing. The spacious and sturdy desktop provides ample room for your workstation.", "Office",
        ["https://placehold.co/600x400/888/FFF?text=Standing+Desk"],
        rating=4.7, reviews=1900,
        features=["Quiet dual-motor electric height adjustment", "4 programmable memory presets for one-touch adjustments", "Spacious desktop for multiple monitors and accessories", "Sturdy steel frame for stability at any height", "Integrated cable management system for a clean workspace"],
        specs={"Type": "Electric Standing Desk", "Height Range": "28-48 inches (71-122 cm)", "Desktop Dimensions": "48 x 30 inches", "Weight Capacity": "220 lbs (100 kg)", "Frame Material": "Steel"}
    ),
    
    # --- Books (Existing) ---
    Product(
        "The Python Guide", 29.99, "A comprehensive, in-depth guide to mastering Python 3. This book covers everything from the basics of the language to advanced topics, with a focus on practical application and best practices in software engineering. It includes numerous code examples and exercises to solidify your understanding.", "Books",
        ["https://placehold.co/600x400/3B82F6/FFF?text=Python+Guide"],
        rating=4.8, reviews=1800,
        features=["Comprehensive coverage of Python 3, from fundamentals to advanced topics", "Practical code examples and exercises to reinforce learning", "Focus on software engineering best practices and project structuring", "Includes guidance on setting up a proper development environment", "Covers the Python Standard Library and object-oriented programming"],
        specs={"Author": "Various", "Pages": "500+", "Language": "English", "Level": "Beginner to Advanced", "Focus": "General Python, Software Engineering"}
    ),
    Product(
        "The Pragmatic Programmer", 45.50, "The 20th Anniversary Edition of the classic book that examines what it means to be a modern programmer. This edition is a complete rewrite, with new tips and a focus on topics from personal responsibility and career development to architectural techniques for flexible and adaptable code.", "Books",
        ["https://placehold.co/600x400/4A5568/FFF?text=Pragmatic+Programmer"],
        rating=4.9, reviews=2500,
        features=["20th Anniversary Edition with fully updated and revised content", "Timeless advice for developers on a wide range of topics", "Practical techniques for writing flexible, adaptable, and dynamic code", "New sections on topics like property-based testing and continuous learning", "Written as a series of self-contained sections with anecdotes and examples"],
        specs={"Author": "David Thomas, Andrew Hunt", "Pages": "350+", "Language": "English", "Edition": "20th Anniversary", "Focus": "Software Engineering, Career Development"}
    )
]
def ensure_minimum_images(product, min_images=3):
    """Ensures a product has at least a minimum number of images, adding placeholders if necessary."""
    num_images = len(product.image_urls)
    if num_images < min_images:
        for i in range(num_images, min_images):
            product.image_urls.append(f"https://placehold.co/600x400/cccccc/000000?text={product.name.replace(' ', '+')}+{i+1}")

image_url_map = {
    "Omega Seamaster Diver 300M": [
      "https://commons.wikimedia.org/wiki/Special:FilePath/Omega-Seamaster-p1020458.jpg",
      "https://commons.wikimedia.org/wiki/Special:FilePath/Detailed_view_on_Omega_Seamaster_chronograph_watch_(300_meters_water_resist).jpg",
      "https://commons.wikimedia.org/wiki/Special:FilePath/Omega_Seamaster_chronograph_watch_(300_meters_water_resist).jpg",
      "https://commons.wikimedia.org/wiki/Special:FilePath/Omega_Seamaster_chronograph_watch_(300_meters_water_resistant)_(cropped).jpg",
      "https://commons.wikimedia.org/wiki/Special:FilePath/Omega_watch_(25263509997).jpg"
    ],
    "Apple iPhone 16": [
      "https://commons.wikimedia.org/wiki/Special:FilePath/IPhone_16_(54251031797).jpg",
      "https://commons.wikimedia.org/wiki/Special:FilePath/Right_view_of_iPhone_16_Pro_Max_Natural_Titanium.jpg",
      "https://commons.wikimedia.org/wiki/Special:FilePath/Back_view_of_iPhone_16_Ultramarine.jpg"
    ],
    "Samsung Galaxy Watch 8": [
      "https://commons.wikimedia.org/wiki/Special:FilePath/Samsung_Galaxy_Watch_8_(Silver).png"
    ],
    "Casio MRW-200H": [
      "https://commons.wikimedia.org/wiki/Special:FilePath/Casio_MRW-200H_001.jpg"
    ],
    "Timex Weekender": [
      "https://commons.wikimedia.org/wiki/Special:FilePath/Timex_Weekender_Indiglo.gif"
    ],
    "Seiko 5 Sports Automatic": [
      "https://commons.wikimedia.org/wiki/Special:FilePath/Seiko_5_Sports_SNZH53K1.jpg",
      "https://commons.wikimedia.org/wiki/Special:FilePath/Seiko_5_Introduction.jpg"
    ],
    "HP Victus 15-fb3004AX": [
        "https://source.unsplash.com/600x400/?gaming,laptop&sig=1",
        "https://source.unsplash.com/600x400/?laptop,keyboard,rgb&sig=2",
        "https://source.unsplash.com/600x400/?hp,laptop&sig=3"
    ],
    "Lenovo ThinkBook 16": [
        "https://source.unsplash.com/600x400/?lenovo,laptop&sig=4",
        "https://source.unsplash.com/600x400/?business,laptop&sig=5",
        "https://source.unsplash.com/600x400/?laptop,desk,office&sig=6"
    ],
    "Apple MacBook Air M2": [
        "https://source.unsplash.com/600x400/?macbook,air&sig=7",
        "https://source.unsplash.com/600x400/?apple,laptop&sig=8",
        "https://source.unsplash.com/600x400/?macbook,desk&sig=9",
        "https://source.unsplash.com/600x400/?silver,laptop&sig=10"
    ],
    "Asus Zenbook 14 OLED (2025)": [
        "https://source.unsplash.com/600x400/?asus,zenbook&sig=11",
        "https://source.unsplash.com/600x400/?oled,laptop&sig=12",
        "https://source.unsplash.com/600x400/?thin,laptop&sig=13"
    ],
    "Dell G15 5530 Gaming Laptop": [
        "https://source.unsplash.com/600x400/?dell,gaming,laptop&sig=14",
        "https://source.unsplash.com/600x400/?gaming,laptop,setup&sig=15",
        "https://source.unsplash.com/600x400/?alienware,laptop&sig=16"
    ],
    "Lenovo LOQ 15IAX9 Gaming Laptop": [
        "https://source.unsplash.com/600x400/?lenovo,legion,laptop&sig=17",
        "https://source.unsplash.com/600x400/?gaming,laptop,blue&sig=18",
        "https://source.unsplash.com/600x400/?esports,laptop&sig=19"
    ],
    "Casio Edifice Chronograph": [
        "https://source.unsplash.com/600x400/?casio,edifice,watch&sig=26",
        "https://source.unsplash.com/600x400/?chronograph,watch&sig=27",
        "https://source.unsplash.com/600x400/?steel,watch&sig=28"
    ],
    "Google Pixel Watch 3": [
        "https://source.unsplash.com/600x400/?pixel,watch&sig=47",
        "https://source.unsplash.com/600x400/?google,smartwatch&sig=48",
        "https://source.unsplash.com/600x400/?smartwatch,minimalist&sig=49"
    ],
    "ASUS ROG Swift OLED PG27UCDM": [
        "https://source.unsplash.com/600x400/?gaming,monitor,rgb&sig=50",
        "https://source.unsplash.com/600x400/?asus,rog,monitor&sig=51",
        "https://source.unsplash.com/600x400/?oled,monitor&sig=52"
    ],
    "Dell U2725QE Office Monitor": [
        "https://source.unsplash.com/600x400/?dell,monitor,office&sig=53",
        "https://source.unsplash.com/600x400/?computer,monitor,desk&sig=54",
        "https://source.unsplash.com/600x400/?4k,monitor&sig=55"
    ],
    "Sony WH-1000XM6": [
        "https://source.unsplash.com/600x400/?sony,headphones&sig=59",
        "https://source.unsplash.com/600x400/?wireless,headphones,black&sig=60",
        "https://source.unsplash.com/600x400/?noise,cancelling,headphones&sig=61"
    ],
    "Bowers & Wilkins Px7 S3": [
        "https://source.unsplash.com/600x400/?premium,headphones&sig=62",
        "https://source.unsplash.com/600x400/?silver,headphones&sig=63",
        "https://source.unsplash.com/600x400/?luxury,audio&sig=64"
    ],
    "Sennheiser HD 660S2 Wired Headphones": [
        "https://source.unsplash.com/600x400/?sennheiser,headphones&sig=65",
        "https://source.unsplash.com/600x400/?audiophile,headphones&sig=66",
        "https://source.unsplash.com/600x400/?open,back,headphones&sig=67"
    ],
    "Timbuk2 Authority Laptop Backpack Deluxe": [
        "https://source.unsplash.com/600x400/?laptop,backpack&sig=68",
        "https://source.unsplash.com/600x400/?commuter,backpack&sig=69",
        "https://source.unsplash.com/600x400/?tech,bag&sig=70"
    ],
    "Cotopaxi Allpa 35L Travel Pack": [
        "https://source.unsplash.com/600x400/?travel,backpack,colorful&sig=71",
        "https://source.unsplash.com/600x400/?cotopaxi,bag&sig=72",
        "https://source.unsplash.com/600x400/?adventure,backpack&sig=73"
    ],
    "Patagonia Black Hole Duffel 55L": [
        "https://source.unsplash.com/600x400/?duffel,bag,travel&sig=74",
        "https://source.unsplash.com/600x400/?patagonia,bag&sig=75",
        "https://source.unsplash.com/600x400/?expedition,bag&sig=76"
    ],
    "Osprey Transporter Duffel 40L": [
        "https://source.unsplash.com/600x400/?osprey,backpack&sig=77",
        "https://source.unsplash.com/600x400/?travel,duffel&sig=78",
        "https://source.unsplash.com/600x400/?green,bag&sig=79"
    ],
    "Moto G96 5G": [
        "https://source.unsplash.com/600x400/?motorola,phone&sig=80",
        "https://source.unsplash.com/600x400/?smartphone,hand&sig=81",
        "https://source.unsplash.com/600x400/?android,phone&sig=82"
    ],
    "Redmi Note 14 SE 5G": [
        "https://source.unsplash.com/600x400/?xiaomi,phone&sig=83",
        "https://source.unsplash.com/600x400/?redmi,smartphone&sig=84",
        "https://source.unsplash.com/600x400/?phone,screen&sig=85"
    ],
    "Samsung Galaxy A35 5G": [
        "https://source.unsplash.com/600x400/?samsung,galaxy,phone&sig=86",
        "https://source.unsplash.com/600x400/?samsung,phone,a-series&sig=87",
        "https://source.unsplash.com/600x400/?smartphone,camera&sig=88"
    ],
    "Google Pixel 9": [
        "https://source.unsplash.com/600x400/?google,pixel,phone&sig=89",
        "https://source.unsplash.com/600x400/?pixel,9&sig=90",
        "https://source.unsplash.com/600x400/?android,smartphone&sig=91"
    ],
    "Intel Core i9-14900K CPU": [
        "https://source.unsplash.com/600x400/?computer,processor&sig=95",
        "https://source.unsplash.com/600x400/?cpu,chip&sig=96",
        "https://source.unsplash.com/600x400/?intel,core,i9&sig=97"
    ],
    "NVIDIA GeForce RTX 4090 GPU": [
        "https://source.unsplash.com/600x400/?graphics,card,nvidia&sig=98",
        "https://source.unsplash.com/600x400/?rtx,4090&sig=99",
        "https://source.unsplash.com/600x400/?pc,component&sig=100"
    ],
    "HyperX Cloud II Headset": [
        "https://source.unsplash.com/600x400/?gaming,headset&sig=101",
        "https://source.unsplash.com/600x400/?hyperx,headphones&sig=102",
        "https://source.unsplash.com/600x400/?red,headset&sig=103"
    ],
    "Secretlab TITAN Evo Gaming Chair": [
        "https://source.unsplash.com/600x400/?gaming,chair&sig=104",
        "https://source.unsplash.com/600x400/?ergonomic,chair&sig=105",
        "https://source.unsplash.com/600x400/?secretlab,chair&sig=106"
    ],
    "High-Speed Blender": [
        "https://source.unsplash.com/600x400/?blender,kitchen&sig=107",
        "https://source.unsplash.com/600x400/?smoothie,maker&sig=108",
        "https://source.unsplash.com/600x400/?kitchen,appliance&sig=109"
    ],
    "Classic Denim Jacket": [
        "https://source.unsplash.com/600x400/?denim,jacket&sig=110",
        "https://source.unsplash.com/600x400/?jean,jacket,fashion&sig=111",
        "https://source.unsplash.com/600x400/?mens,fashion&sig=112"
    ],
    "Cordless Stick Vacuum": [
        "https://source.unsplash.com/600x400/?cordless,vacuum&sig=113",
        "https://source.unsplash.com/600x400/?vacuum,cleaner&sig=114",
        "https://source.unsplash.com/600x400/?cleaning,home&sig=115"
    ],
    "Egyptian Cotton Sheet Set Queen": [
        "https://source.unsplash.com/600x400/?bed,sheets,white&sig=116",
        "https://source.unsplash.com/600x400/?cotton,bedding&sig=117",
        "https://source.unsplash.com/600x400/?luxury,bedding&sig=118"
    ],
    "The Pragmatic Programmer": [
        "https://source.unsplash.com/600x400/?programming,book&sig=119",
        "https://source.unsplash.com/600x400/?book,code&sig=120",
        "https://source.unsplash.com/600x400/?bookshelf,tech&sig=121"
    ]
}

# for product in products_list:
#     if product.name in image_url_map:
#         product.image_urls = image_url_map[product.name]
#     ensure_minimum_images(product)

# Convert any dictionaries in the product list to Product objects
for i, p in enumerate(products_list):
    if isinstance(p, dict):
        products_list[i] = Product(p['name'], p['price'], p['description'], p['category'], p['image_urls'], rating=p['rating'], reviews=p['reviews'], features=p['features'], specs=p['specs'])

products_dict = {p.product_id: p for p in products_list}
all_categories = sorted(list(set(p.category for p in products_list)))

# --- HTML Templates ---

BASE_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Amazon Clone{% endblock %}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://kit.fontawesome.com/852cc0f4e1.js" crossorigin="anonymous"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style> 
        body { font-family: 'Inter', sans-serif; background-color: #f3f4f6; -webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale; }
        .btn-amazon { background-color: #FF9900; border-color: #a88734 #9c7e31 #846a29; color: #111; border-width: 1px; border-style: solid; transition: all 0.2s ease; }
        .btn-amazon:hover { background-color: #FFA500; }
        .btn-amazon:active { transform: translateY(1px); }
        .btn-secondary { background-color: #FFA500; }
        .btn-secondary:hover { background-color: #FFB733; }
        #flyout-menu { transform: translateX(-100%); transition: transform 0.3s ease-in-out; }
        #flyout-menu.open { transform: translateX(0); }
        #flyout-overlay { transition: opacity 0.3s ease-in-out; }
        .group:hover .group-hover\:block { display: block; }
        .star-rating { color: #FF9900; }
    </style>
</head>
<body class="bg-gray-100">
    <!-- Main Header -->
    <header class="bg-[#232f3e] text-white shadow-lg sticky top-0 z-20">
        <div class="container mx-auto flex items-center p-2 text-sm">
            <a href="/" class="p-2 border border-transparent hover:border-white rounded-sm inline-block" style="line-height: 0;">
                <div style="position: relative; width: 97px; height: 30px;">
                    <!-- Amazon text -->
                    <span style="display: inline-block; font-family: Arial, sans-serif; font-size: 28px; font-weight: bold; color: white; letter-spacing: -1px; line-height: 1;">amazon</span>
                    <!-- Smile arrow positioned absolutely below text -->
                    <svg style="position: absolute; bottom: -2px; left: 0; width: 97px; height: 8px;" viewBox="0 0 97 8" xmlns="http://www.w3.org/2000/svg">
                        <path d="M 2 4 Q 48.5 8, 95 4" stroke="#FF9900" stroke-width="2" fill="none" stroke-linecap="round"/>
                        <path d="M 93.5 2.5 L 97 4 L 93.5 5.5" fill="#FF9900"/>
                    </svg>
                </div>
            </a>
            <a href="#" class="flex items-center p-2 ml-4 border border-transparent hover:border-white rounded-sm"><i class="fa-solid fa-location-dot mr-1"></i><div><span class="text-xs text-gray-300">Deliver to</span><span class="font-bold">India</span></div></a>
            <form action="/search" method="get" class="hidden sm:flex flex-grow mx-4 items-center">
                <div class="relative group">
                    <button type="button" class="bg-gray-100 rounded-l-md p-2 text-gray-700 text-xs font-medium hover:bg-gray-200 flex items-center">
                        All <i class="fa-solid fa-caret-down ml-1"></i>
                    </button>
                    <div class="absolute hidden group-hover:block bg-white text-gray-800 mt-0 rounded-md shadow-lg z-30 w-48 left-0 top-full">
                        <a href="#" class="block px-4 py-2 text-sm hover:bg-gray-100">All Departments</a>
                        <a href="#" class="block px-4 py-2 text-sm hover:bg-gray-100">Laptops</a>
                        <a href="#" class="block px-4 py-2 text-sm hover:bg-gray-100">Watches</a>
                        <a href="#" class="block px-4 py-2 text-sm hover:bg-gray-100">Smartwatches</a>
                        <a href="#" class="block px-4 py-2 text-sm hover:bg-gray-100">Monitors</a>
                        <a href="#" class="block px-4 py-2 text-sm hover:bg-gray-100">Headphones</a>
                        <a href="#" class="block px-4 py-2 text-sm hover:bg-gray-100">Gaming Components</a>
                        <a href="#" class="block px-4 py-2 text-sm hover:bg-gray-100">Gaming Peripherals</a>
                        <a href="#" class="block px-4 py-2 text-sm hover:bg-gray-100">Smartphones</a>
                    </div>
                </div>
                <input type="text" name="query" placeholder="Search Amazon Clone..." class="w-full p-2 text-gray-800 focus:outline-none text-base border-t border-b border-gray-300">
                <button type="submit" class="bg-[#febd69] hover:bg-[#f3a847] p-2 rounded-r-md">
                    <i class="fa-solid fa-magnifying-glass text-gray-800 text-xl"></i>
                </button>
            </form>
                        <div class="relative group">
                {% if current_user %}
                    <a href="#" class="p-2 border border-transparent hover:border-white rounded-sm">
                        <span class="text-xs">Hello, {{ current_user.name }}</span>
                        <span class="font-bold flex items-center">Account & Lists <i class="fa-solid fa-caret-down ml-1"></i></span>
                    </a>
                    <div class="absolute hidden group-hover:block bg-white text-black mt-1 p-4 rounded-md shadow-lg z-30 w-60 right-0">
                        <h3 class="font-bold mb-2">Your Account</h3>
                        <a href="{{ url_for('orders_page') }}" class="block hover:underline mb-1">Your Orders</a>
                        <a href="{{ url_for('wishlist_page') }}" class="block hover:underline mb-1">Your Wish List</a>
                        <a href="{{ url_for('recommendations_page') }}" class="block hover:underline mb-1">Your Recommendations</a>
                        <a href="/logout" class="block hover:underline">Sign Out</a>
                    </div>
                {% else %}
                    <a href="/signin" class="p-2 border border-transparent hover:border-white rounded-sm">
                        <span class="text-xs">Hello, sign in</span>
                        <span class="font-bold flex items-center">Account & Lists <i class="fa-solid fa-caret-down ml-1"></i></span>
                    </a>
                    <div class="absolute hidden group-hover:block bg-white text-black mt-1 p-4 rounded-md shadow-lg z-30 w-60 right-0">
                        <h3 class="font-bold mb-2">Your Account</h3>
                        <a href="{{ url_for('orders_page') }}" class="block hover:underline mb-1">Your Orders</a>
                        <a href="{{ url_for('wishlist_page') }}" class="block hover:underline mb-1">Your Wish List</a>
                        <a href="{{ url_for('recommendations_page') }}" class="block hover:underline mb-1">Your Recommendations</a>
                        <a href="/signin" class="block hover:underline">Sign In</a>
                    </div>
                {% endif %}
            </div>
            <a href="{{ url_for('orders_page') }}" class="p-2 ml-2 border border-transparent hover:border-white rounded-sm"><span class="text-xs">Returns</span><span class="font-bold">& Orders</span></a>
            <a href="/cart" class="flex items-end p-2 ml-2 border border-transparent hover:border-white rounded-sm"><i class="fa-solid fa-cart-shopping text-2xl"></i><span class="font-bold text-yellow-400 ml-1">{{ cart_item_count }}</span><span class="font-bold ml-1">Cart</span></a>
        </div>
    </header>

    <!-- Sub Navigation -->
    <nav class="bg-gray-700 text-white text-sm font-semibold p-2 shadow-md sticky top-[68px] z-10">
        <div class="container mx-auto flex items-center">
            <button id="all-menu-btn" class="flex items-center p-1 border border-transparent hover:border-white rounded-sm"><i class="fa-solid fa-bars mr-1"></i> All</button>
            <a href="/deals" class="p-1 ml-2 border border-transparent hover:border-white rounded-sm">Today's Deals</a>
            <a href="#" class="p-1 ml-2 border border-transparent hover:border-white rounded-sm">Customer Service</a>
        </div>
    </nav>
    
    <!-- Flyout Menu -->
    <div id="flyout-overlay" class="fixed inset-0 bg-black bg-opacity-50 z-30 hidden"></div>
    <div id="flyout-menu" class="fixed top-0 left-0 h-full w-80 bg-white shadow-lg z-40 overflow-y-auto">
        <div class="bg-gray-800 text-white p-4 flex justify-between items-center"><h2 class="text-xl font-bold">Shop by Department</h2><button id="close-flyout-btn"><i class="fa-solid fa-times text-2xl"></i></button></div>
        <div class="p-4">{% for category in all_categories %}<a href="/category/{{ category|replace(' ', '%20') }}" class="block py-2 px-4 hover:bg-gray-200 rounded-md">{{ category }}</a>{% endfor %}</div>
    </div>

    {% with messages = get_flashed_messages(with_categories=true) %}{% if messages %}<div class="container mx-auto mt-4 p-4 sm:p-0">{% for category, message in messages %}<div class="{{ 'bg-green-500' if category == 'success' else 'bg-red-500' }} text-white text-center p-2 rounded-lg mb-2 shadow-md">{{ message }}</div>{% endfor %}</div>{% endif %}{% endwith %}

    <main class="container mx-auto mt-4 p-4 sm:p-0">{% block content %}{% endblock %}</main>
    
    <footer class="bg-gray-800 text-white mt-8">
    <div id="back-to-top" class="bg-gray-700 hover:bg-gray-600 cursor-pointer">
        <p class="text-center p-3">Back to top</p>
    </div>
    <div class="container mx-auto grid grid-cols-2 md:grid-cols-4 gap-8 p-8">
        <div>
            <h3 class="font-bold mb-2">Get to Know Us</h3>
            <ul>
                <li class="mb-1"><a href="#" class="text-gray-300 hover:text-white">Careers</a></li>
                <li class="mb-1"><a href="#" class="text-gray-300 hover:text-white">Blog</a></li>
                <li class="mb-1"><a href="#" class="text-gray-300 hover:text-white">About Amazon</a></li>
                <li class="mb-1"><a href="#" class="text-gray-300 hover:text-white">Investor Relations</a></li>
                <li class="mb-1"><a href="#" class="text-gray-300 hover:text-white">Amazon Devices</a></li>
                <li class="mb-1"><a href="#" class="text-gray-300 hover:text-white">Amazon Science</a></li>
            </ul>
        </div>
        <div>
            <h3 class="font-bold mb-2">Make Money with Us</h3>
            <ul>
                <li class="mb-1"><a href="#" class="text-gray-300 hover:text-white">Sell products on Amazon</a></li>
                <li class="mb-1"><a href="#" class="text-gray-300 hover:text-white">Sell on Amazon Business</a></li>
                <li class="mb-1"><a href="#" class="text-gray-300 hover:text-white">Sell apps on Amazon</a></li>
                <li class="mb-1"><a href="#" class="text-gray-300 hover:text-white">Become an Affiliate</a></li>
                <li class="mb-1"><a href="#" class="text-gray-300 hover:text-white">Advertise Your Products</a></li>
                <li class="mb-1"><a href="#" class="text-gray-300 hover:text-white">Self-Publish with Us</a></li>
                <li class="mb-1"><a href="#" class="text-gray-300 hover:text-white">Host an Amazon Hub</a></li>
                <li class="mb-1"><a href="#" class="text-gray-300 hover:text-white">› See More Make Money with Us</a></li>
            </ul>
        </div>
        <div>
            <h3 class="font-bold mb-2">Amazon Payment Products</h3>
            <ul>
                <li class="mb-1"><a href="#" class="text-gray-300 hover:text-white">Amazon Business Card</a></li>
                <li class="mb-1"><a href="#" class="text-gray-300 hover:text-white">Shop with Points</a></li>
                <li class="mb-1"><a href="#" class="text-gray-300 hover:text-white">Reload Your Balance</a></li>
                <li class="mb-1"><a href="#" class="text-gray-300 hover:text-white">Amazon Currency Converter</a></li>
            </ul>
        </div>
        <div>
            <h3 class="font-bold mb-2">Let Us Help You</h3>
            <ul>
                <li class="mb-1"><a href="#" class="text-gray-300 hover:text-white">Amazon and COVID-19</a></li>
                <li class="mb-1"><a href="{{ url_for('orders_page') }}" class="text-gray-300 hover:text-white">Your Account</a></li>
                <li class="mb-1"><a href="{{ url_for('orders_page') }}" class="text-gray-300 hover:text-white">Your Orders</a></li>
                <li class="mb-1"><a href="#" class="text-gray-300 hover:text-white">Shipping Rates & Policies</a></li>
                <li class="mb-1"><a href="#" class="text-gray-300 hover:text-white">Returns & Replacements</a></li>
                <li class="mb-1"><a href="#" class="text-gray-300 hover:text-white">Manage Your Content and Devices</a></li>
                <li class="mb-1"><a href="#" class="text-gray-300 hover:text-white">Help</a></li>
            </ul>
        </div>
    </div>
    <div class="bg-gray-900 py-6">
        <div class="container mx-auto text-center">
            <img src="https://placehold.co/100x30/fff/000?text=amazon" alt="Amazon Logo" class="mx-auto mb-4">
            <div class="flex justify-center items-center space-x-4 text-sm">
                <form action="/set_locale" method="post" class="flex justify-center items-center space-x-4 text-sm">
                    <div class="flex items-center space-x-2">
                        <label for="language" class="sr-only">Language</label>
                        <select name="language" id="language" onchange="this.form.submit()" class="bg-gray-700 border border-gray-500 rounded-sm px-3 py-1 hover:bg-gray-600 cursor-pointer">
                            <option value="en_US" {% if session.get('language') == 'en_US' %}selected{% endif %}>🇺🇸 English</option>
                            <option value="es_MX" {% if session.get('language') == 'es_MX' %}selected{% endif %}>🇲🇽 Español</option>
                            <option value="fr_CA" {% if session.get('language') == 'fr_CA' %}selected{% endif %}>🇨🇦 Français</option>
                            <option value="de_DE" {% if session.get('language') == 'de_DE' %}selected{% endif %}>🇩🇪 Deutsch</option>
                            <option value="ja_JP" {% if session.get('language') == 'ja_JP' %}selected{% endif %}>🇯🇵 日本語</option>
                        </select>
                    </div>
                    <div class="flex items-center space-x-2">
                        <label for="currency" class="sr-only">Currency</label>
                        <select name="currency" id="currency" onchange="this.form.submit()" class="bg-gray-700 border border-gray-500 rounded-sm px-3 py-1 hover:bg-gray-600 cursor-pointer">
                            <option value="USD" {% if session.get('currency') == 'USD' %}selected{% endif %}>$ USD - U.S. Dollar</option>
                            <option value="INR" {% if session.get('currency') == 'INR' %}selected{% endif %}>₹ INR - Indian Rupee</option>
                            <option value="EUR" {% if session.get('currency') == 'EUR' %}selected{% endif %}>€ EUR - Euro</option>
                            <option value="JPY" {% if session.get('currency') == 'JPY' %}selected{% endif %}>¥ JPY - Japanese Yen</option>
                            <option value="GBP" {% if session.get('currency') == 'GBP' %}selected{% endif %}>£ GBP - British Pound</option>
                        </select>
                    </div>
                </form>
            </div>
        </div>
    </div>
    <div class="bg-gray-900 text-white p-8">
        <div class="container mx-auto grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-7 gap-4 text-xs">
            <div><a href="#" class="hover:underline"><div>Amazon Music</div><div class="text-gray-400">Stream millions of songs</div></a></div>
            <div><a href="#" class="hover:underline"><div>Amazon Ads</div><div class="text-gray-400">Reach customers wherever they spend their time</div></a></div>
            <div><a href="#" class="hover:underline"><div>6pm</div><div class="text-gray-400">Score deals on fashion brands</div></a></div>
            <div><a href="#" class="hover:underline"><div>AbeBooks</div><div class="text-gray-400">Books, art & collectibles</div></a></div>
            <div><a href="#" class="hover:underline"><div>ACX</div><div class="text-gray-400">Audiobook Publishing Made Easy</div></a></div>
            <div><a href="#" class="hover:underline"><div>Sell on Amazon</div><div class="text-gray-400">Start a Selling Account</div></a></div>
            <div><a href="#" class="hover:underline"><div>Veeqo</div><div class="text-gray-400">Shipping Software Inventory Management</div></a></div>
            <div><a href="#" class="hover:underline"><div>Amazon Business</div><div class="text-gray-400">Everything For Your Business</div></a></div>
            <div><a href="#" class="hover:underline"><div>AmazonGlobal</div><div class="text-gray-400">Ship Orders Internationally</div></a></div>
            <div><a href="#" class="hover:underline"><div>Amazon Web Services</div><div class="text-gray-400">Scalable Cloud Computing Services</div></a></div>
            <div><a href="#" class="hover:underline"><div>Audible</div><div class="text-gray-400">Listen to Books & Original Audio Performances</div></a></div>
            <div><a href="#" class="hover:underline"><div>Box Office Mojo</div><div class="text-gray-400">Find Movie Box Office Data</div></a></div>
            <div><a href="#" class="hover:underline"><div>Goodreads</div><div class="text-gray-400">Book reviews & recommendations</div></a></div>
            <div><a href="#" class="hover:underline"><div>IMDb</div><div class="text-gray-400">Movies, TV & Celebrities</div></a></div>
            <div><a href="#" class="hover:underline"><div>IMDbPro</div><div class="text-gray-400">Get Info Entertainment Professionals Need</div></a></div>
            <div><a href="#" class="hover:underline"><div>Kindle Direct Publishing</div><div class="text-gray-400">Indie Digital & Print Publishing Made Easy</div></a></div>
            <div><a href="#" class="hover:underline"><div>Prime Video Direct</div><div class="text-gray-400">Video Distribution Made Easy</div></a></div>
            <div><a href="#" class="hover:underline"><div>Shopbop</div><div class="text-gray-400">Designer Fashion Brands</div></a></div>
            <div><a href="#" class="hover:underline"><div>Woot!</div><div class="text-gray-400">Deals and Shenanigans</div></a></div>
            <div><a href="#" class="hover:underline"><div>Zappos</div><div class="text-gray-400">Shoes & Clothing</div></a></div>
            <div><a href="#" class="hover:underline"><div>Ring</div><div class="text-gray-400">Smart Home Security Systems</div></a></div>
            <div><a href="#" class="hover:underline"><div>eero WiFi</div><div class="text-gray-400">Stream 4K Video in Every Room</div></a></div>
            <div><a href="#" class="hover:underline"><div>Blink</div><div class="text-gray-400">Smart Security for Every Home</div></a></div>
            <div><a href="#" class="hover:underline"><div>Neighbors App</div><div class="text-gray-400">Real-Time Crime & Safety Alerts</div></a></div>
            <div><a href="#" class="hover:underline"><div>Amazon Subscription Boxes</div><div class="text-gray-400">Top subscription boxes - right to your door</div></a></div>
            <div><a href="#" class="hover:underline"><div>PillPack</div><div class="text-gray-400">Pharmacy Simplified</div></a></div>
        </div>
    </div>
    <div class="bg-gray-900 p-6 text-center text-gray-400 text-xs">
        <div class="flex justify-center space-x-4 mb-2">
            <a href="#" class="hover:underline">Conditions of Use</a>
            <a href="#" class="hover:underline">Privacy Notice</a>
            <a href="#" class="hover:underline">Consumer Health Data Privacy Disclosure</a>
            <a href="#" class="hover:underline">Your Ads Privacy Choices</a>
        </div>
        <p>&copy; 1996-2025, Amazon.clone, Inc. or its affiliates</p>
    </div>
</footer>
    <script>
        document.getElementById('back-to-top').addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
        const allMenuBtn = document.getElementById('all-menu-btn');
        if(allMenuBtn) {
            const closeFlyoutBtn = document.getElementById('close-flyout-btn');
            const flyoutMenu = document.getElementById('flyout-menu');
            const flyoutOverlay = document.getElementById('flyout-overlay');
            const openFlyout = () => { flyoutMenu.classList.add('open'); flyoutOverlay.classList.remove('hidden'); };
            const closeFlyout = () => { flyoutMenu.classList.remove('open'); flyoutOverlay.classList.add('hidden'); };
            allMenuBtn.addEventListener('click', openFlyout);
            closeFlyoutBtn.addEventListener('click', closeFlyout);
            flyoutOverlay.addEventListener('click', closeFlyout);
        }
        function changeMainImage(newSrc) {
            const mainImage = document.getElementById('main-image');
            if (mainImage) {
                mainImage.src = newSrc;
            }
        }
        document.addEventListener('DOMContentLoaded', function () {
            const cardNumberInput = document.getElementById('card_number');
            if (cardNumberInput) {
                cardNumberInput.addEventListener('input', formatCardNumber);
            }

            const checkoutForm = document.querySelector('form[action="/place_order"]');
            if (checkoutForm) {
                validateForm(checkoutForm);
            }
        });

        function formatCardNumber(event) {
            const input = event.target;
            let value = input.value.replace(/\D/g, '');
            let formattedValue = '';
            for (let i = 0; i < value.length; i++) {
                if (i > 0 && i % 4 === 0) {
                    formattedValue += ' ';
                }
                formattedValue += value[i];
            }
            input.value = formattedValue;
        }

        function validateForm(form) {
            form.addEventListener('submit', function(event) {
                if (!form.checkValidity()) {
                    event.preventDefault();
                    event.stopPropagation();
                }

                Array.from(form.elements).forEach(function(element) {
                    const errorSpan = element.nextElementSibling;
                    if (errorSpan && errorSpan.tagName === 'SPAN') {
                        if (element.validity.valueMissing) {
                            errorSpan.textContent = 'This field is required.';
                        } else if (element.validity.patternMismatch) {
                            errorSpan.textContent = `Please match the requested format. ${element.placeholder ? `e.g., ${element.placeholder}` : ''}`;
                        } else {
                            errorSpan.textContent = '';
                        }
                    }
                });

                form.classList.add('was-validated');
            }, false);
        }
    </script>
</body>
</html>
"""

HOME_PAGE_TEMPLATE = """
{% extends 'base.html' %}
{% block title %}Homepage - Amazon Clone{% endblock %}
{% block content %}
<!-- Main Carousel -->
<div id="carousel" class="relative rounded-lg shadow-xl overflow-hidden mb-8">
    <div class="relative h-56 md:h-96 overflow-hidden">{% for slide in carousel_slides %}<div class="carousel-item hidden duration-700 ease-in-out"><a href="{{ slide.link }}"><img src="{{ slide.image }}" class="absolute block w-full -translate-x-1/2 -translate-y-1/2 top-1/2 left-1/2" alt="{{ slide.title }}"></a></div>{% endfor %}</div>
    <button type="button" id="carousel-prev" class="absolute top-0 left-0 z-10 flex items-center justify-center h-full px-4 group"><span class="carousel-control inline-flex items-center justify-center w-10 h-10 rounded-full"><svg class="w-4 h-4 text-white" fill="none" viewBox="0 0 6 10"><path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 1 1 5l4 4"/></svg></span></button>
    <button type="button" id="carousel-next" class="absolute top-0 right-0 z-10 flex items-center justify-center h-full px-4 group"><span class="carousel-control inline-flex items-center justify-center w-10 h-10 rounded-full"><svg class="w-4 h-4 text-white" fill="none" viewBox="0 0 6 10"><path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m1 9 4-4-4-4"/></svg></span></button>
</div>

<!-- Category Cards -->
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
    <div class="bg-white rounded-lg shadow-xl p-4 flex flex-col"><h2 class="text-xl font-bold text-gray-800 mb-4">Get your game on</h2><a href="/category/Gaming%20Components" class="flex-grow"><img src="https://placehold.co/600x600/1a1a1a/ffffff?text=High-Performance+Gaming+Gear" alt="Gaming Setup" class="w-full h-full object-cover rounded-md"></a></div>
    <div class="bg-white rounded-lg shadow-xl p-4 flex flex-col"><h2 class="text-xl font-bold text-gray-800 mb-4">Refresh your space</h2><div class="grid grid-cols-2 gap-4 flex-grow"><div><a href="/category/Kitchenware"><img src="https://placehold.co/300x300/E5E7EB/000?text=Modern+Dining" class="w-full h-auto object-cover rounded-md"></a><a href="/category/Kitchenware" class="text-sm hover:underline">Dining</a></div><div><a href="/category/Home%20Decor"><img src="https://placehold.co/300x300/D1D5DB/000?text=Cozy+Home" class="w-full h-auto object-cover rounded-md"></a><a href="/category/Home%20Decor" class="text-sm hover:underline">Home Decor</a></div><div><a href="/category/Kitchenware"><img src="https://placehold.co/300x300/9CA3AF/000?text=Stylish+Kitchen" class="w-full h-auto object-cover rounded-md"></a><a href="/category/Kitchenware" class="text-sm hover:underline">Kitchen</a></div><div><a href="/category/Makeup%20&%20Beauty"><img src="https://placehold.co/300x300/6B7280/FFF?text=Beauty+Care" class="w-full h-auto object-cover rounded-md"></a><a href="/category/Makeup%20&%20Beauty" class="text-sm hover:underline">Beauty & Personal Care</a></div></div></div>
    <div class="bg-white rounded-lg shadow-xl p-4 flex flex-col"><h2 class="text-xl font-bold text-gray-800 mb-4">Shop for your home essentials</h2><div class="grid grid-cols-2 gap-4 flex-grow"><div><a href="/category/Cleaning%20Supplies"><img src="https://placehold.co/300x300/F3F4F6/000?text=Cleaning+Tools" class="w-full h-auto object-cover rounded-md"></a><a href="/category/Cleaning%20Supplies" class="text-sm hover:underline">Cleaning Supplies</a></div><div><a href="/category/Home%20Storage"><img src="https://placehold.co/300x300/E5E7EB/000?text=Smart+Storage" class="w-full h-auto object-cover rounded-md"></a><a href="/category/Home%20Storage" class="text-sm hover:underline">Home Storage</a></div><div><a href="/category/Home%20Decor"><img src="https://placehold.co/300x300/D1D5DB/000?text=Chic+Decor" class="w-full h-auto object-cover rounded-md"></a><a href="/category/Home%20Decor" class="text-sm hover:underline">Home Decor</a></div><div><a href="/category/Bedding"><img src="https://placehold.co/300x300/9CA3AF/000?text=Comfy+Bedding" class="w-full h-auto object-cover rounded-md"></a><a href="/category/Bedding" class="text-sm hover:underline">Bedding</a></div></div></div>
</div>

<!-- Product Carousels -->
<div class="space-y-8">
    <div class="bg-white rounded-lg shadow-xl p-6"><h2 class="text-2xl font-bold text-gray-800 mb-4">Trending Products</h2><div class="relative"><div id="trending-carousel" class="flex overflow-x-auto space-x-4" style="scrollbar-width: none; -ms-overflow-style: none;">{% for product in trending_products %}<div class="flex-shrink-0 w-48 product-card-hover bg-gray-50 p-2 rounded-lg"><a href="/product/{{ product.product_id }}"><img src="{{ product.image_urls[0].replace('600x400', '300x300') }}" alt="{{ product.name }}" class="w-full h-32 object-cover rounded-md mb-2"><h3 class="text-sm font-semibold truncate">{{ product.name }}</h3><p class="text-lg font-bold">{{ currency_symbol }}{{ "%.2f"|format(product.price) }}</p></a></div>{% endfor %}</div><button id="trending-prev" class="absolute top-1/2 -translate-y-1/2 -left-4 bg-white/80 p-2 rounded-full shadow-md z-10 hover:bg-white"><i class="fa-solid fa-chevron-left"></i></button><button id="trending-next" class="absolute top-1/2 -translate-y-1/2 -right-4 bg-white/80 p-2 rounded-full shadow-md z-10 hover:bg-white"><i class="fa-solid fa-chevron-right"></i></button></div></div>
    <div class="bg-white rounded-lg shadow-xl p-6"><h2 class="text-2xl font-bold text-gray-800 mb-4">Best Seller Mobiles</h2><div class="relative"><div id="mobiles-carousel" class="flex overflow-x-auto space-x-4" style="scrollbar-width: none; -ms-overflow-style: none;">{% for product in smartphones %}<div class="flex-shrink-0 w-48 product-card-hover bg-gray-50 p-2 rounded-lg"><a href="/product/{{ product.product_id }}"><img src="{{ product.image_urls[0].replace('600x400', '300x300') }}" alt="{{ product.name }}" class="w-full h-32 object-cover rounded-md mb-2"><h3 class="text-sm font-semibold truncate">{{ product.name }}</h3><p class="text-lg font-bold">{{ currency_symbol }}{{ "%.2f"|format(product.price) }}</p></a></div>{% endfor %}</div><button id="mobiles-prev" class="absolute top-1/2 -translate-y-1/2 -left-4 bg-white/80 p-2 rounded-full shadow-md z-10 hover:bg-white"><i class="fa-solid fa-chevron-left"></i></button><button id="mobiles-next" class="absolute top-1/2 -translate-y-1/2 -right-4 bg-white/80 p-2 rounded-full shadow-md z-10 hover:bg-white"><i class="fa-solid fa-chevron-right"></i></button></div></div>
    <div class="bg-white rounded-lg shadow-xl p-6"><h2 class="text-2xl font-bold text-gray-800 mb-4">Top Picks in Laptops</h2><div class="relative"><div id="laptops-carousel" class="flex overflow-x-auto space-x-4" style="scrollbar-width: none; -ms-overflow-style: none;">{% for product in laptops %}<div class="flex-shrink-0 w-48 product-card-hover bg-gray-50 p-2 rounded-lg"><a href="/product/{{ product.product_id }}"><img src="{{ product.image_urls[0].replace('600x400', '300x300') }}" alt="{{ product.name }}" class="w-full h-32 object-cover rounded-md mb-2"><h3 class="text-sm font-semibold truncate">{{ product.name }}</h3><p class="text-lg font-bold">${{ "%.2f"|format(product.price) }}</p></a></div>{% endfor %}</div><button id="laptops-prev" class="absolute top-1/2 -translate-y-1/2 -left-4 bg-white/80 p-2 rounded-full shadow-md z-10 hover:bg-white"><i class="fa-solid fa-chevron-left"></i></button><button id="laptops-next" class="absolute top-1/2 -translate-y-1/2 -right-4 bg-white/80 p-2 rounded-full shadow-md z-10 hover:bg-white"><i class="fa-solid fa-chevron-right"></i></button></div></div>
    <div class="bg-white rounded-lg shadow-xl p-6"><h2 class="text-2xl font-bold text-gray-800 mb-4">Popular Watches</h2><div class="relative"><div id="watches-carousel" class="flex overflow-x-auto space-x-4" style="scrollbar-width: none; -ms-overflow-style: none;">{% for product in watches %}<div class="flex-shrink-0 w-48 product-card-hover bg-gray-50 p-2 rounded-lg"><a href="/product/{{ product.product_id }}"><img src="{{ product.image_urls[0].replace('600x400', '300x300') }}" alt="{{ product.name }}" class="w-full h-32 object-cover rounded-md mb-2"><h3 class="text-sm font-semibold truncate">{{ product.name }}</h3><p class="text-lg font-bold">${{ "%.2f"|format(product.price) }}</p></a></div>{% endfor %}</div><button id="watches-prev" class="absolute top-1/2 -translate-y-1/2 -left-4 bg-white/80 p-2 rounded-full shadow-md z-10 hover:bg-white"><i class="fa-solid fa-chevron-left"></i></button><button id="watches-next" class="absolute top-1/2 -translate-y-1/2 -right-4 bg-white/80 p-2 rounded-full shadow-md z-10 hover:bg-white"><i class="fa-solid fa-chevron-right"></i></button></div></div>
</div>

<script>
    document.addEventListener('DOMContentLoaded', function () {
        const carousel = document.getElementById('carousel');
        if (carousel) {
            const items = carousel.querySelectorAll('.carousel-item');
            if (items.length > 0) {
                const prevButton = document.getElementById('carousel-prev');
                const nextButton = document.getElementById('carousel-next');
                let currentItem = 0; let slideInterval;
                const showItem = (i) => items.forEach((item, idx) => item.classList.toggle('hidden', i !== idx));
                const next = () => { currentItem = (currentItem + 1) % items.length; showItem(currentItem); };
                const prev = () => { currentItem = (currentItem - 1 + items.length) % items.length; showItem(currentItem); };
                const start = () => slideInterval = setInterval(next, 5000);
                const stop = () => clearInterval(slideInterval);
                showItem(0); start();
                nextButton.addEventListener('click', () => { stop(); next(); start(); });
                prevButton.addEventListener('click', () => { stop(); prev(); start(); });
            }
        }
        function setupScroller(cId, pId, nId) {
            const c = document.getElementById(cId);
            if(c) {
                document.getElementById(nId).addEventListener('click', () => c.scrollBy({ left: 300, behavior: 'smooth' }));
                document.getElementById(pId).addEventListener('click', () => c.scrollBy({ left: -300, behavior: 'smooth' }));
            }
        }
        setupScroller('trending-carousel', 'trending-prev', 'trending-next');
        setupScroller('mobiles-carousel', 'mobiles-prev', 'mobiles-next');
        setupScroller('laptops-carousel', 'laptops-prev', 'laptops-next');
        setupScroller('watches-carousel', 'watches-prev', 'watches-next');
    });
</script>
{% endblock %}
"""

CATEGORY_PAGE_TEMPLATE = """
{% extends 'base.html' %}
{% block title %}{{ category_name }} - Amazon Clone{% endblock %}
{% block content %}
<a href="/" class="text-sm text-blue-600 hover:underline mb-6 inline-block">&larr; Back to Homepage</a>
<h2 class="text-3xl font-bold text-gray-800 mb-6">Products in {{ category_name }}</h2>
{% if products %}<div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
    {% for product in products %}<div class="bg-white rounded-lg shadow-lg overflow-hidden flex flex-col product-card-hover"><a href="/product/{{ product.product_id }}"><img src="{{ product.image_urls[0] }}" alt="Image of {{ product.name }}" class="w-full h-48 object-cover"></a><div class="p-4 flex flex-col flex-grow"><h3 class="text-lg font-semibold text-gray-900">{{ product.name }}</h3><p class="text-sm text-gray-500 mb-2">{{ product.category }}</p><div class="mt-auto flex justify-between items-center pt-4"><p class="text-xl font-bold text-gray-900">{{ currency_symbol }}{{ "%.2f"|format(product.price) }}</p><a href="/product/{{ product.product_id }}" class="bg-gray-200 hover:bg-gray-300 text-gray-800 font-bold py-2 px-4 rounded-lg text-sm">View</a></div></div></div>{% endfor %}
</div>{% else %}<div class="bg-white rounded-lg shadow-lg p-8 text-center"><p class="text-gray-600">There are no products in this category yet.</p></div>{% endif %}
{% endblock %}
"""

SEARCH_RESULTS_PAGE_TEMPLATE = """
{% extends 'base.html' %}
{% block title %}Search Results - Amazon Clone{% endblock %}
{% block content %}
<a href="/" class="text-sm text-blue-600 hover:underline mb-6 inline-block">&larr; Back to Homepage</a>
<h2 class="text-3xl font-bold text-gray-800 mb-2">Search Results for "{{ query }}"</h2><p class="text-gray-600 mb-6">{{ results|length }} items found.</p>
{% if results %}<div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
    {% for product in results %}<div class="bg-white rounded-lg shadow-lg overflow-hidden flex flex-col product-card-hover"><a href="/product/{{ product.product_id }}"><img src="{{ product.image_urls[0] }}" alt="Image of {{ product.name }}" class="w-full h-48 object-cover"></a><div class="p-4 flex flex-col flex-grow"><h3 class="text-lg font-semibold text-gray-900">{{ product.name }}</h3><p class="text-sm text-gray-500 mb-2">{{ product.category }}</p><div class="mt-auto flex justify-between items-center pt-4"><p class="text-xl font-bold text-gray-900">{{ currency_symbol }}{{ "%.2f"|format(product.price) }}</p><a href="/product/{{ product.product_id }}" class="bg-gray-200 hover:bg-gray-300 text-gray-800 font-bold py-2 px-4 rounded-lg text-sm">View</a></div></div></div>{% endfor %}
</div>{% else %}<div class="bg-white rounded-lg shadow-lg p-8 text-center"><p class="text-gray-600">No products found matching your search.</p></div>{% endif %}
{% endblock %}
"""

PRODUCT_PAGE_TEMPLATE = """
{% extends 'base.html' %}
{% block title %}{{ product.name }} - Amazon Clone{% endblock %}
{% block content %}
<div class="bg-white rounded-lg shadow-xl overflow-hidden">
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 p-4">
        <!-- Image Gallery -->
        <div class="lg:col-span-1 flex">
            <div class="flex flex-col space-y-2 mr-2">
                {% for img_url in product.image_urls %}
                <img src="{{ img_url.replace('600x400', '100x100') }}" alt="thumbnail" class="w-12 h-12 object-cover rounded-md cursor-pointer border-2 hover:border-yellow-500" onclick="changeMainImage('{{ img_url.replace('100x100', '800x600') }}')">
                {% endfor %}
            </div>
            <div>
                <img id="main-image" src="{{ product.image_urls[0].replace('100x100', '800x600') }}" alt="Main image of {{ product.name }}" class="w-full h-auto object-contain rounded-lg">
            </div>
        </div>

        <!-- Product Info -->
        <div class="lg:col-span-1">
            <a href="{{ url_for('category_page', category_name=product.category|replace(' ', '%20')) }}" class="text-sm text-blue-600 hover:underline mb-2 block">{{ product.category }}</a>
            <h1 class="text-2xl font-bold text-gray-900 mb-2">{{ product.name }}</h1>
            <div class="flex items-center mb-4"><span class="star-rating"){% for i in range(product.rating|round|int) %}<i class="fa-solid fa-star"></i>{% endfor %}{% if product.rating - product.rating|round|int >= 0.5 %}<i class="fa-solid fa-star-half-alt"></i>{% endif %}</span><span class="ml-2 text-sm text-blue-600 hover:underline">{{ product.reviews }} ratings</span></div>
            <div class="text-3xl font-bold text-gray-900 mb-4">{{ currency_symbol }}{{ "%.2f"|format(product.price) }}</div>
            <h2 class="font-bold text-lg mb-2">About this item</h2>
            <ul class="list-disc list-inside text-gray-700 space-y-1">
                {% for feature in product.features %}<li>{{ feature }}</li>{% endfor %}
            </ul>
        </div>
        
        <!-- Buy Box -->
        <div class="lg:col-span-1 border-2 border-gray-200 rounded-lg p-4 h-fit">
            <div class="text-2xl font-bold text-gray-900 mb-2">{{ currency_symbol }}{{ "%.2f"|format(product.price) }}</div>
            <p class="text-sm text-gray-600">Ships from: <span class="font-semibold">Amazon Clone</span></p>
            <p class="text-green-600 font-bold my-2">In Stock</p>
            <form action="/add_to_cart/{{ product.product_id }}" method="post" class="space-y-4">
                <div class="flex items-center">
                    <label for="quantity" class="mr-2">Qty:</label>
                    <select name="quantity" id="quantity" class="p-2 border rounded-md">
                        {% for i in range(1, 11) %}<option value="{{i}}">{{i}}</option>{% endfor %}
                    </select>
                </div>
                <button type="submit" class="w-full btn-amazon font-bold py-2 rounded-lg">Add to Cart</button>
                <button type="submit" formaction="/add_to_cart/{{ product.product_id }}?buy_now=true" class="w-full btn-amazon btn-secondary font-bold py-2 rounded-lg">Buy Now</button>
            </form>
        </div>
    </div>

    <!-- Product Details Section -->
    <div class="p-8">
        <h2 class="text-2xl font-bold text-gray-800 mb-4 border-b pb-2">Product information</h2>
        <table class="w-full text-sm">
            <tbody>
                {% for key, value in product.specs.items() %}
                <tr class="border-b">
                    <th class="text-left font-semibold p-2 bg-gray-100 w-1/3">{{ key }}</th>
                    <td class="p-2">{{ value }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</div>
{% endblock %}
"""

CART_PAGE_TEMPLATE = """
{% extends 'base.html' %}
{% block title %}Shopping Cart - Amazon Clone{% endblock %}
{% block content %}
<h2 class="text-3xl font-bold text-gray-800 mb-6">Your Shopping Cart</h2>
{% if not cart_items %}
    <div class="bg-white rounded-lg shadow-lg p-8 text-center"><p class="text-gray-600">Your cart is empty.</p><a href="/" class="mt-4 inline-block bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-lg">Continue Shopping</a></div>
{% else %}
<div class="grid grid-cols-1 md:grid-cols-3 gap-8">
    <div class="md:col-span-2 bg-white rounded-lg shadow-lg">
        <ul class="divide-y divide-gray-200">
            {% for item in cart_items %}
            <li class="p-4 flex items-center justify-between">
                <div class="flex items-center">
                    <img src="{{ item.product.image_urls[0].replace('600x400', '150x100') }}" alt="{{ item.product.name }}" class="h-16 w-24 object-cover rounded-md mr-4">
                    <div><p class="font-semibold text-gray-800">{{ item.product.name }}</p><p class="text-sm text-gray-500">{{ currency_symbol }}{{ "%.2f"|format(item.product.price) }}</p></div>
                </div>
                <div class="flex items-center">
                    <form action="/update_cart/{{ item.product.product_id }}" method="post" class="flex items-center">
                        <label for="quantity-{{item.product.product_id}}" class="text-sm mr-2">Qty:</label>
                        <input type="number" id="quantity-{{item.product.product_id}}" name="quantity" value="{{ item.quantity }}" min="0" class="w-16 p-1 border rounded-md mr-2">
                        <button type="submit" class="text-blue-600 hover:underline text-sm">Update</button>
                    </form>
                    <form action="/remove_from_cart/{{ item.product.product_id }}" method="post" class="ml-4">
                        <button type="submit" class="text-red-500 hover:text-red-700 font-semibold">Remove</button>
                    </form>
                </div>
            </li>
            {% endfor %}
        </ul>
    </div>
    <div class="bg-white rounded-lg shadow-lg p-6 h-fit">
        <h3 class="text-lg font-bold mb-4">Order Summary</h3>
        <div class="flex justify-between mb-2"><span>Subtotal ({{ cart_item_count }} items)</span><span>{{ currency_symbol }}{{ "%.2f"|format(total_price) }}</span></div>
        <div class="flex justify-between font-bold text-xl border-t pt-4 mt-4"><span>Order total</span><span>{{ currency_symbol }}{{ "%.2f"|format(total_price) }}</span></div>
        <a href="/checkout" class="block w-full text-center mt-6 btn-amazon font-bold py-2 px-4 rounded-lg">Proceed to Checkout</a>
    </div>
</div>
{% endif %}
{% endblock %}
"""

SIGN_IN_PAGE_TEMPLATE = """
{% extends 'base.html' %}
{% block title %}Sign-In - Amazon Clone{% endblock %}
{% block content %}
<div class="max-w-md mx-auto bg-white rounded-lg shadow-md p-8">
    <h2 class="text-2xl font-bold text-center mb-6">Sign-In</h2><form action="/login" method="post"><div class="mb-4"><label for="email" class="block text-sm font-medium text-gray-700">Email</label><input type="email" name="email" id="email" class="mt-1 block w-full px-3 py-2 border rounded-md shadow-sm focus:outline-none" required></div><div class="mb-6"><label for="password" class="block text-sm font-medium text-gray-700">Password</label><input type="password" name="password" id="password" class="mt-1 block w-full px-3 py-2 border rounded-md shadow-sm focus:outline-none" required></div><button type="submit" class="w-full btn-amazon font-bold py-2 px-4 rounded-lg">Sign In</button><p class="text-xs text-gray-600 mt-4">By signing-in you agree to Amazon Clone's Conditions of Use & Sale.</p><div class="mt-6 text-center"><a href="#" class="text-sm text-blue-600 hover:underline">Create your Amazon account</a></div></form>
</div>
{% endblock %}
"""

CHECKOUT_PAGE_TEMPLATE = """
{% extends 'base.html' %}
{% block title %}Checkout - Amazon Clone{% endblock %}
{% block content %}
<div class="grid grid-cols-1 md:grid-cols-3 gap-8">
    <div class="md:col-span-2 bg-white rounded-lg shadow-lg p-6">
        <h2 class="text-2xl font-bold mb-6">Checkout</h2>
        <form action="/place_order" method="post" novalidate>
            <h3 class="text-lg font-bold mb-4 border-b pb-2">1. Shipping Address</h3>
            <div class="grid grid-cols-2 gap-4">
                <div>
                    <label for="full_name" class="block text-sm">Full Name</label>
                    <input type="text" id="full_name" name="full_name" class="w-full border p-2 rounded-md" required pattern="[A-Za-z\s]+" placeholder="e.g., John Doe">
                    <span class="text-red-500 text-xs"></span>
                </div>
                <div>
                    <label for="phone_number" class="block text-sm">Phone Number</label>
                    <div class="flex">
                        <select name="country_code" class="border p-2 rounded-l-md">
                            <option value="+91">+91 (IN)</option>
                            <option value="+1">+1 (US)</option>
                        </select>
                        <input type="tel" id="phone_number" name="phone_number" class="w-full border p-2 rounded-r-md" required pattern="[0-9]{10}" placeholder="9876543210">
                    </div>
                    <span class="text-red-500 text-xs"></span>
                </div>
                <div class="col-span-2">
                    <label for="address" class="block text-sm">Address</label>
                    <input type="text" id="address" name="address" class="w-full border p-2 rounded-md" required placeholder="e.g., 123, Main Street">
                    <span class="text-red-500 text-xs"></span>
                </div>
                <div>
                    <label for="city" class="block text-sm">City</label>
                    <input type="text" id="city" name="city" class="w-full border p-2 rounded-md" required pattern="[A-Za-z\s]+" placeholder="e.g., Mumbai">
                    <span class="text-red-500 text-xs"></span>
                </div>
                <div>
                    <label for="state_province" class="block text-sm">State / Province</label>
                    <input type="text" id="state_province" name="state_province" class="w-full border p-2 rounded-md" required pattern="[A-Za-z\s]+" placeholder="e.g., Maharashtra">
                    <span class="text-red-500 text-xs"></span>
                </div>
                <div>
                    <label for="zip_code" class="block text-sm">ZIP / Postal Code</label>
                    <input type="tel" id="zip_code" name="zip_code" class="w-full border p-2 rounded-md" required pattern="[0-9]{6}" placeholder="123456">
                    <span class="text-red-500 text-xs"></span>
                </div>
            </div>
            <h3 class="text-lg font-bold mb-4 border-b pb-2 mt-8">2. Payment Method</h3>
            <div>
                <label for="card_number" class="block text-sm">Card Number</label>
                <input type="tel" name="card_number" id="card_number" class="w-full border p-2 rounded-md" required pattern="[0-9\s]{15,19}" placeholder="xxxx xxxx xxxx xxxx">
                <span class="text-red-500 text-xs"></span>
            </div>
             <div class="grid grid-cols-2 gap-4 mt-4">
                <div>
                    <label for="expiration_date" class="block text-sm">Expiration Date</label>
                    <input type="text" id="expiration_date" name="expiration_date" placeholder="MM/YY" class="w-full border p-2 rounded-md" required pattern="(0[1-9]|1[0-2])\/[0-9]{2}">
                    <span class="text-red-500 text-xs"></span>
                </div>
                <div>
                    <label for="cvv" class="block text-sm">CVV</label>
                    <input type="tel" id="cvv" name="cvv" class="w-full border p-2 rounded-md" required pattern="[0-9]{3,4}" placeholder="123">
                    <span class="text-red-500 text-xs"></span>
                </div>
            </div>
            <div class="md:col-span-2 p-6 h-fit">
                <button type="submit" class="w-full text-center mt-6 btn-amazon font-bold py-2 px-4 rounded-lg">Place Your Order</button>
            </div>
        </form>
    </div>
    <div class="bg-white rounded-lg shadow-lg p-6 h-fit">
        <h3 class="text-lg font-bold mb-4">Order Summary</h3>
        {% for item in cart_items %}<div class="flex justify-between items-center mb-2 text-sm"><span class="truncate w-40">{{ item.product.name }} (x{{ item.quantity }})</span><span>{{ currency_symbol }}{{ "%.2f"|format(item.product.price * item.quantity) }}</span></div>{% endfor %}
        <div class="flex justify-between font-bold text-xl border-t pt-4 mt-4"><span>Order total</span><span>{{ currency_symbol }}{{ "%.2f"|format(total_price) }}</span></div>
        <form action="/place_order" method="post" class="hidden md:block">
            <button type="submit" class="w-full text-center mt-6 btn-amazon font-bold py-2 px-4 rounded-lg">Place Your Order</button>
        </form>
    </div>
</div>
{% endblock %}
"""

ORDER_CONFIRMATION_PAGE_TEMPLATE = """
{% extends 'base.html' %}
{% block title %}Order Confirmed - Amazon Clone{% endblock %}
{% block content %}
<div class="max-w-2xl mx-auto bg-white rounded-lg shadow-md p-8 text-center">
    <i class="fa-solid fa-check-circle text-6xl text-green-500 mb-4"></i>
    <h2 class="text-3xl font-bold mb-4">Thank You for Your Order!</h2>
    <p class="text-gray-600 mb-2">Your order has been placed successfully.</p>
    <p class="text-gray-600 mb-6">Your Order ID is: <span class="font-semibold">{{ order.order_id }}</span></p>
    <a href="/" class="btn-amazon font-bold py-2 px-6 rounded-lg">Continue Shopping</a>
</div>
{% endblock %}
"""

DEALS_PAGE_TEMPLATE = """
{% extends 'base.html' %}
{% block title %}Deals - Amazon Clone{% endblock %}
{% block content %}
<h2 class="text-3xl font-bold text-gray-800 mb-6">Today's Deals</h2>
<div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
    {% for product in deals_products %}
    <div class="bg-white rounded-lg shadow-lg overflow-hidden flex flex-col product-card-hover">
        <a href="/product/{{ product.product_id }}"><img src="{{ product.image_urls[0] }}" alt="Image of {{ product.name }}" class="w-full h-48 object-cover"></a>
        <div class="p-4 flex flex-col flex-grow">
            <h3 class="text-lg font-semibold text-gray-900">{{ product.name }}</h3>
            <div class="mt-auto flex justify-between items-center pt-4">
                <p class="text-xl font-bold text-red-600">{{ currency_symbol }}{{ "%.2f"|format(product.price * 0.8) }}</p>
                <p class="text-sm text-gray-500 line-through">{{ currency_symbol }}{{ "%.2f"|format(product.price) }}</p>
            </div>
        </div>
    </div>
    {% endfor %}
</div>
{% endblock %}
"""

ORDERS_PAGE_TEMPLATE = """
{% extends 'base.html' %}
{% block title %}Your Orders - Amazon Clone{% endblock %}
{% block content %}
<div class="max-w-4xl mx-auto bg-white rounded-lg shadow-md p-8">
    <h2 class="text-3xl font-bold mb-6">Your Orders</h2>
    {% if orders %}
        <div class="space-y-4">
            {% for order in orders %}
                <div class="border rounded-lg p-4">
                    <div class="flex justify-between items-center mb-2">
                        <h3 class="text-lg font-semibold">Order ID: {{ order.order_id }}</h3>
                        <p class="text-sm text-gray-500">Placed on: {{ order.order_date.strftime('%Y-%m-%d') }}</p>
                    </div>
                    <div class="flex justify-between items-center">
                        <p class="text-lg font-bold">Total: {{ currency_symbol }}{{ "%.2f"|format(order.total_price) }}</p>
                    </div>
                    <div class="mt-4">
                        <h4 class="font-semibold">Items:</h4>
                        <ul class="list-disc list-inside">
                            {% for item in order.items %}
                                <li>{{ item.product.name }} (x{{ item.quantity }})</li>
                            {% endfor %}
                        </ul>
                    </div>
                </div>
            {% endfor %}
        </div>
    {% else %}
        <div class="text-center text-gray-500">
            <p>You have no past orders.</p>
            <a href="/" class="mt-4 inline-block btn-amazon font-bold py-2 px-4 rounded-lg">Continue Shopping</a>
        </div>
    {% endif %}
</div>
{% endblock %}
"""

WISHLIST_PAGE_TEMPLATE = """
{% extends 'base.html' %}
{% block title %}Wish List - Amazon Clone{% endblock %}
{% block content %}
<div class="max-w-4xl mx-auto bg-white rounded-lg shadow-md p-8">
    <h2 class="text-3xl font-bold mb-6">Your Wish List</h2>
    <div class="text-center text-gray-500">
        <p>Your wish list is empty.</p>
    </div>
</div>
{% endblock %}
"""

RECOMMENDATIONS_PAGE_TEMPLATE = """
{% extends 'base.html' %}
{% block title %}Recommendations - Amazon Clone{% endblock %}
{% block content %}
<div class="max-w-4xl mx-auto bg-white rounded-lg shadow-md p-8">
    <h2 class="text-3xl font-bold mb-6">Your Recommendations</h2>
    <p class="text-gray-500">We'll have recommendations for you once you start shopping.</p>
</div>
{% endblock %}
"""

app.jinja_loader = DictLoader({
    'base.html': BASE_TEMPLATE,
    'home.html': HOME_PAGE_TEMPLATE,
    'category.html': CATEGORY_PAGE_TEMPLATE,
    'search_results.html': SEARCH_RESULTS_PAGE_TEMPLATE,
    'product.html': PRODUCT_PAGE_TEMPLATE,
    'cart.html': CART_PAGE_TEMPLATE,
    'signin.html': SIGN_IN_PAGE_TEMPLATE,
    'checkout.html': CHECKOUT_PAGE_TEMPLATE,
    'order_confirmation.html': ORDER_CONFIRMATION_PAGE_TEMPLATE,
    'deals.html': DEALS_PAGE_TEMPLATE,
    'orders.html': ORDERS_PAGE_TEMPLATE,
    'wishlist.html': WISHLIST_PAGE_TEMPLATE,
    'recommendations.html': RECOMMENDATIONS_PAGE_TEMPLATE
})

@app.context_processor
def inject_user():
    user_id = session.get('user_id')
    if user_id:
        user = users_by_id.get(user_id)
        return dict(current_user=user)
    return dict(current_user=None)

# --- Helper Function ---
def get_cart_details():
    """Retrieves cart from session and calculates details."""
    cart = session.get('cart', {})
    cart_items, total_price, item_count = [], 0, 0
    for product_id, quantity in cart.items():
        product = products_dict.get(product_id)
        if product:
            cart_items.append({'product': product, 'quantity': quantity})
            total_price += product.price * quantity
            item_count += quantity
    return cart_items, total_price, item_count

# --- Routes ---

@app.route('/')
def homepage():
    """Renders the homepage."""
    _, _, cart_item_count = get_cart_details()
    carousel_slides = [
        {"image": "https://placehold.co/1200x500/000000/FFFFFF?text=Gaming+Store", "title": "Gaming Store", "link": url_for('category_page', category_name='Gaming Components')},
        {"image": "https://placehold.co/1200x500/F59E0B/FFFFFF?text=Kitchen+Essentials", "title": "Kitchen Essentials", "link": url_for('category_page', category_name='Kitchenware')},
        {"image": "https://placehold.co/1200x500/EC4899/FFFFFF?text=Latest+Fashion", "title": "Fashion Finds", "link": url_for('category_page', category_name='Fashion')}
    ]
    fashion_products = [p for p in products_list if p.category == 'Fashion']
    smartphones = [p for p in products_list if p.category == 'Smartphones']
    laptops = [p for p in products_list if p.category == 'Laptops']
    watches = [p for p in products_list if p.category == 'Watches']
    trending_products = sorted([p for p in products_list if p.category not in ['Laptops', 'Smartphones', 'Watches']], key=lambda x: x.reviews, reverse=True)[:15]

    return render_template('home.html', cart_item_count=cart_item_count, carousel_slides=carousel_slides, trending_products=trending_products, all_categories=all_categories, fashion_products=fashion_products, smartphones=smartphones, laptops=laptops, watches=watches)

@app.route('/category/<category_name>')
def category_page(category_name):
    """Renders a page for a specific category."""
    _, _, cart_item_count = get_cart_details()
    category_products = [p for p in products_list if p.category == category_name]
    return render_template('category.html', products=category_products, category_name=category_name, cart_item_count=cart_item_count, all_categories=all_categories)

@app.route('/search')
def search_page():
    """Handles search queries."""
    query = request.args.get('query', '')
    _, _, cart_item_count = get_cart_details()
    search_results = [p for p in products_list if query.lower() in p.name.lower() or query.lower() in p.description.lower() or query.lower() in p.category.lower()] if query else []
    return render_template('search_results.html', results=search_results, query=query, cart_item_count=cart_item_count, all_categories=all_categories)

@app.route('/product/<product_id>')
def product_page(product_id):
    """Renders a single product page."""
    _, _, cart_item_count = get_cart_details()
    product = products_dict.get(product_id)
    return render_template('product.html', product=product, cart_item_count=cart_item_count, all_categories=all_categories) if product else abort(404)

@app.route('/add_to_cart/<product_id>', methods=['POST'])
def add_to_cart(product_id):
    """Adds an item to the cart."""
    product = products_dict.get(product_id)
    if not product: abort(404)
    quantity = int(request.form.get('quantity', 1))
    cart = session.get('cart', {})
    cart[product_id] = cart.get(product_id, 0) + quantity
    session['cart'] = cart
    flash(f'Added {quantity} x "{product.name}" to your cart!', 'success')
    return redirect(url_for('checkout_page')) if 'buy_now' in request.args else redirect(url_for('product_page', product_id=product_id))

@app.route('/remove_from_cart/<product_id>', methods=['POST'])
def remove_from_cart(product_id):
    """Removes an item from the cart."""
    cart = session.get('cart', {})
    if product_id in cart:
        product_name = products_dict.get(product_id).name
        cart.pop(product_id)
        session['cart'] = cart
        flash(f'"{product_name}" has been removed from your cart.', 'danger')
    return redirect(url_for('cart_page'))

@app.route('/update_cart/<product_id>', methods=['POST'])
def update_cart(product_id):
    """Updates an item's quantity in the cart."""
    cart = session.get('cart', {})
    quantity = int(request.form.get('quantity', 1))
    if product_id in cart:
        if quantity > 0:
            cart[product_id] = quantity
            flash(f'Updated quantity for "{products_dict.get(product_id).name}".', 'success')
        else:
            cart.pop(product_id)
            flash(f'"{products_dict.get(product_id).name}" has been removed.', 'danger')
        session['cart'] = cart
    return redirect(url_for('cart_page'))

@app.route('/cart')
def cart_page():
    """Displays the shopping cart page."""
    cart_items, total_price, cart_item_count = get_cart_details()
    return render_template('cart.html', cart_items=cart_items, total_price=total_price, cart_item_count=cart_item_count, all_categories=all_categories)

@app.route('/signin')
def signin_page():
    """Displays the sign-in page."""
    _, _, cart_item_count = get_cart_details()
    return render_template('signin.html', cart_item_count=cart_item_count, all_categories=all_categories)

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    user = users_dict.get(email)
    if user and user.password == password:
        session['user_id'] = user.id
        flash('You have been logged in!', 'success')
        return redirect(url_for('homepage'))
    else:
        flash('Invalid email or password.', 'danger')
        return redirect(url_for('signin_page'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('homepage'))

@app.route('/checkout')
def checkout_page():
    """Displays the checkout page."""
    cart_items, total_price, cart_item_count = get_cart_details()
    return redirect(url_for('homepage')) if not cart_items else render_template('checkout.html', cart_items=cart_items, total_price=total_price, cart_item_count=cart_item_count, all_categories=all_categories)

@app.route('/place_order', methods=['POST'])
def place_order():
    """Handles placing an order, including validation and order creation."""
    # Server-side validation
    required_fields = ['full_name', 'phone_number', 'address', 'city', 'state_province', 'zip_code', 'card_number', 'expiration_date', 'cvv']
    for field in required_fields:
        if not request.form.get(field):
            flash(f'Please fill out all required fields.', 'danger')
            return redirect(url_for('checkout_page'))

    # Get user and cart details
    user_id = session.get('user_id')
    if not user_id:
        flash('You must be logged in to place an order.', 'danger')
        return redirect(url_for('signin_page'))

    cart_items, total_price, _ = get_cart_details()
    if not cart_items:
        flash('Your cart is empty.', 'danger')
        return redirect(url_for('homepage'))

    # Create and store the order
    new_order = Order(user_id=user_id, items=cart_items, total_price=total_price)
    orders_list.append(new_order)

    # Clear the cart
    session.pop('cart', None)

    flash('Your order has been placed successfully!', 'success')
    return redirect(url_for('order_confirmation', order_id=new_order.order_id))

@app.route('/order_confirmation')
def order_confirmation():
    """Displays the order confirmation page."""
    order_id = request.args.get('order_id')
    order = next((o for o in orders_list if o.order_id == order_id), None)
    if not order:
        return redirect(url_for('homepage'))
    _, _, cart_item_count = get_cart_details()
    return render_template('order_confirmation.html', order=order, cart_item_count=cart_item_count, all_categories=all_categories)

@app.route('/deals')
def deals_page():
    """Displays the 'Today's Deals' page."""
    _, _, cart_item_count = get_cart_details()
    # Populate deals with a diverse range of products
    deals_products = [p for p in products_list if p.category in ["Smartphones", "Laptops", "Watches", "Headphones", "Gaming Components", "Fashion", "Home Decor"]][:10]
    return render_template('deals.html', deals_products=deals_products, cart_item_count=cart_item_count, all_categories=all_categories)

# Placeholder routes for account links
@app.route('/orders')
def orders_page():
    user_id = session.get('user_id')
    if not user_id:
        flash('You must be logged in to view your orders.', 'danger')
        return redirect(url_for('signin_page'))
    
    user_orders = [order for order in orders_list if order.user_id == user_id]
    _, _, cart_item_count = get_cart_details()
    return render_template('orders.html', orders=user_orders, cart_item_count=cart_item_count, all_categories=all_categories)

@app.route('/wishlist')
def wishlist_page():
    _, _, cart_item_count = get_cart_details()
    return render_template('wishlist.html', cart_item_count=cart_item_count, all_categories=all_categories)

@app.route('/recommendations')
def recommendations_page():
    _, _, cart_item_count = get_cart_details()
    return render_template('recommendations.html', cart_item_count=cart_item_count, all_categories=all_categories)


# --- Main Execution ---

if __name__ == "__main__":
    app.run(debug=True, port=5001)
