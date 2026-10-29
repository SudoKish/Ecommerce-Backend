from django.core.management.base import BaseCommand
from store.models import Category, Product

class Command(BaseCommand):
    help = 'Seeds initial Anand Mangal Sports catalog data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Seeding Anand Mangal Sports data..."))

        # Clean existing
        Product.objects.all().delete()
        Category.objects.all().delete()

        categories_data = [
            {
                'name': 'Running',
                'slug': 'running',
                'description': 'Engineered for relentless pace, carbon propulsion, and nitrogen-infused cushioning.',
                'icon_name': 'Zap',
                'image_url': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=800&auto=format&fit=crop&q=80'
            },
            {
                'name': 'Cricket',
                'slug': 'cricket',
                'description': 'Grade 1 English Willow bats, protective batting armor, and tournament grade leather balls.',
                'icon_name': 'Shield',
                'image_url': 'https://images.unsplash.com/photo-1540747913346-19e32dc3e97e?w=800&auto=format&fit=crop&q=80'
            },
            {
                'name': 'Football',
                'slug': 'football',
                'description': 'Precision speed boots, aerodynamic match balls, and elite grip turf gear.',
                'icon_name': 'Target',
                'image_url': 'https://images.unsplash.com/photo-1511886929837-354d827aae26?w=800&auto=format&fit=crop&q=80'
            },
            {
                'name': 'Gym & Training',
                'slug': 'training',
                'description': 'Sweat-wicking dry-cell apparel, hyper-stability lifting trainers, and heavy-duty duffels.',
                'icon_name': 'Activity',
                'image_url': 'https://images.unsplash.com/photo-1517838277536-f5f99be501cd?w=800&auto=format&fit=crop&q=80'
            },
            {
                'name': 'Badminton',
                'slug': 'badminton',
                'description': 'Aerodynamic isometric carbon frames, high-speed nylon & feather shuttles, court grip shoes.',
                'icon_name': 'Award',
                'image_url': 'https://images.unsplash.com/photo-1626224583764-f87db24ac4ea?w=800&auto=format&fit=crop&q=80'
            },
            {
                'name': 'Motorsport & Lifestyle',
                'slug': 'lifestyle',
                'description': 'High-velocity track jackets, race-inspired kicks, and bold streetwear staples.',
                'icon_name': 'Flame',
                'image_url': 'https://images.unsplash.com/photo-1552346154-21d32810aba3?w=800&auto=format&fit=crop&q=80'
            },
        ]

        cat_map = {}
        for cdata in categories_data:
            cat, _ = Category.objects.get_or_create(
                slug=cdata['slug'],
                defaults=cdata
            )
            cat_map[cdata['slug']] = cat

        products_data = [
            # Running Shoes & Gear
            {
                'name': 'AMS Velocity Nitro 3 Road Runners',
                'slug': 'ams-velocity-nitro-3',
                'category': cat_map['running'],
                'sport': 'Running',
                'gender': 'UNISEX',
                'price': 7999.00,
                'original_price': 11999.00,
                'badge': 'BEST SELLER',
                'rating': 4.9,
                'reviews_count': 148,
                'description': 'Our flagship road runner powered by dual-density NITROFOAM™ elite bounce technology. Designed for marathon training, daily tempo runs, and ultra-durable traction on Indian roads.',
                'features': ['NITROFOAM™ nitrogen-infused midsole', 'PUMAGRIP rubber outsole for all-weather traction', 'Breathable engineered mesh upper', 'Reflective heel accents for dawn/night runs'],
                'tech_specs': {'Drop': '10mm', 'Weight': '240g', 'Cushioning': 'Max Plush', 'Terrain': 'Road & Track'},
                'primary_image': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=800&auto=format&fit=crop&q=80',
                'secondary_image': 'https://images.unsplash.com/photo-1608231387042-66d1773070a5?w=800&auto=format&fit=crop&q=80',
                'available_sizes': ['UK 7', 'UK 8', 'UK 9', 'UK 10', 'UK 11'],
                'colors': ['Electric Crimson / Jet Black', 'Neon Volt / Silver'],
                'in_stock': True,
                'is_featured': True
            },
            {
                'name': 'AMS Deviate Carbon Elite Race Kicks',
                'slug': 'ams-deviate-carbon-elite',
                'category': cat_map['running'],
                'sport': 'Running',
                'gender': 'MEN',
                'price': 14499.00,
                'original_price': 18999.00,
                'badge': 'CARBON PROPULSION',
                'rating': 5.0,
                'reviews_count': 89,
                'description': 'Championship-grade racing shoe featuring a full-length spoon-shaped INNOPLATE carbon fiber plate engineered for maximum energy return and blistering half and full marathon pace.',
                'features': ['Full-length INNOPLATE 100% pure carbon plate', 'Ultra-featherweight mono-mesh single layer', 'Hyper-rebound super critical foam', 'Reinforced heel stability frame'],
                'tech_specs': {'Drop': '8mm', 'Weight': '195g', 'Plate': 'Carbon Fiber', 'Purpose': 'Race Day'},
                'primary_image': 'https://images.unsplash.com/photo-1595950653106-6c9ebd614d3a?w=800&auto=format&fit=crop&q=80',
                'secondary_image': 'https://images.unsplash.com/photo-1584735935682-2f2b69dff9d2?w=800&auto=format&fit=crop&q=80',
                'available_sizes': ['UK 7', 'UK 8', 'UK 9', 'UK 10', 'UK 11', 'UK 12'],
                'colors': ['Acid Lime / High Risk Red', 'Pure Platinum'],
                'in_stock': True,
                'is_featured': True
            },
            {
                'name': 'AMS Speed Aero Running Singlet',
                'slug': 'ams-speed-aero-singlet',
                'category': cat_map['running'],
                'sport': 'Running',
                'gender': 'UNISEX',
                'price': 1299.00,
                'original_price': 1999.00,
                'badge': 'NEW DROP',
                'rating': 4.7,
                'reviews_count': 42,
                'description': 'Featherweight moisture-wicking racing singlet engineered with laser-cut ventilation ports. Keeps you dry and cool under extreme summer race temperatures.',
                'features': ['DRYCELL moisture management', 'Anti-friction bonded seams', '360-degree reflectivity', 'Ultra-fast dry micro-poly knit'],
                'tech_specs': {'Fabric': '88% Recycled Poly, 12% Elastane', 'Fit': 'Athletic Slim', 'Care': 'Machine wash cold'},
                'primary_image': 'https://images.unsplash.com/photo-1581655353564-df123a1eb820?w=800&auto=format&fit=crop&q=80',
                'secondary_image': 'https://images.unsplash.com/photo-1503342217505-b0a15ec3261c?w=800&auto=format&fit=crop&q=80',
                'available_sizes': ['S', 'M', 'L', 'XL'],
                'colors': ['Racing Black / Neon Trim', 'Solar Orange'],
                'in_stock': True,
                'is_featured': False
            },

            # Cricket Gear
            {
                'name': 'Anand Mangal Pro Grade 1 English Willow Cricket Bat',
                'slug': 'ams-pro-grade-1-cricket-bat',
                'category': cat_map['cricket'],
                'sport': 'Cricket',
                'gender': 'MEN',
                'price': 13999.00,
                'original_price': 19999.00,
                'badge': 'HAND CRAFTED',
                'rating': 4.9,
                'reviews_count': 165,
                'description': 'Mastercrafted from unbleached hand-selected Grade 1 English Willow. Engineered with an enlarged mid-to-low sweet spot, massive 40mm thick edges, and a feather-light pickup tailored for devastating power hitting.',
                'features': ['Grade 1 English Willow with 8-12 straight grains', 'Full profile spine with duckbill toe design', '12-piece cane treble spring handle', 'Pre-knocked with toe guard applied'],
                'tech_specs': {'Weight': '1170g - 1200g', 'Profile': 'Mid-Low Sweet Spot', 'Handle': 'Semi-Oval Cane', 'Grip': 'Octopus Hex Grip'},
                'primary_image': 'https://images.unsplash.com/photo-1540747913346-19e32dc3e97e?w=800&auto=format&fit=crop&q=80',
                'secondary_image': 'https://images.unsplash.com/photo-1531415074868-036b107e775a?w=800&auto=format&fit=crop&q=80',
                'available_sizes': ['Short Handle (SH)', 'Harrow', 'Size 6'],
                'colors': ['Natural Willow / Stealth Gold', 'Red / Metallic Chrome'],
                'in_stock': True,
                'is_featured': True
            },
            {
                'name': 'AMS Shield Pro Batting Leg Guards & Pads',
                'slug': 'ams-shield-pro-batting-pads',
                'category': cat_map['cricket'],
                'sport': 'Cricket',
                'gender': 'UNISEX',
                'price': 3499.00,
                'original_price': 4999.00,
                'badge': 'TEST MATCH GRADE',
                'rating': 4.8,
                'reviews_count': 56,
                'description': 'Ultra-lightweight high-density molded foam batting pads engineered to withstand 150 km/h fast bowling impacts without sacrificing runner agility.',
                'features': ['Triple layer cane & high density plastazote rods', 'Gel-zone knee bolster for comfort', 'Padded ergonomic quick-release straps', 'Hard-wearing reinforced instep'],
                'tech_specs': {'Weight': '780g per pad', 'Material': 'Imported Matte PU', 'Facing': 'Traditional 7 Cane'},
                'primary_image': 'https://images.unsplash.com/photo-1512719355462-e755517260a0?w=800&auto=format&fit=crop&q=80',
                'secondary_image': 'https://images.unsplash.com/photo-1540747913346-19e32dc3e97e?w=800&auto=format&fit=crop&q=80',
                'available_sizes': ['Men Standard', 'Youth', 'Large Adult'],
                'colors': ['Puma White / Stealth Carbon', 'Navy Blue'],
                'in_stock': True,
                'is_featured': False
            },
            {
                'name': 'AMS Crimson Match Leather Cricket Balls (Pack of 4)',
                'slug': 'ams-crimson-match-balls-pack-4',
                'category': cat_map['cricket'],
                'sport': 'Cricket',
                'gender': 'UNISEX',
                'price': 2199.00,
                'original_price': 2999.00,
                'badge': 'BCCI REGULATION',
                'rating': 4.7,
                'reviews_count': 74,
                'description': 'Four-piece alum-tanned premium steer hide leather balls with Portuguese cork core and 85 hand-stitched seams. Exceptional swing retention and seam prominence for 50+ overs.',
                'features': ['Alum tanned top-grain cowhide leather', 'Four-piece construction with thick center seam', 'High-density layered Portuguese cork core', 'Weatherproof nitro wax polish'],
                'tech_specs': {'Weight': '156g', 'Seam': '80-85 Hand Stitches', 'Pieces': '4 Piece'},
                'primary_image': 'https://images.unsplash.com/photo-1587280501635-68a0e82cd5ff?w=800&auto=format&fit=crop&q=80',
                'secondary_image': 'https://images.unsplash.com/photo-1540747913346-19e32dc3e97e?w=800&auto=format&fit=crop&q=80',
                'available_sizes': ['Standard Senior 5.5oz'],
                'colors': ['Classic Red', 'White T20', 'Pink Day-Night'],
                'in_stock': True,
                'is_featured': False
            },

            # Football / Soccer
            {
                'name': 'AMS Ultra Match FG/AG Football Boots',
                'slug': 'ams-ultra-match-fg-ag',
                'category': cat_map['football'],
                'sport': 'Football',
                'gender': 'UNISEX',
                'price': 6499.00,
                'original_price': 8999.00,
                'badge': 'EXPLOSIVE SPEED',
                'rating': 4.9,
                'reviews_count': 112,
                'description': 'Fast just got faster. The AMS Ultra Match packs lightweight mesh upper reinforced with GripControl skin for decisive ball mastery and an ultra-fast TPU SPEEDPLATE outsole.',
                'features': ['GripControl skin for decisive control when on the attack', 'Lightweight mesh upper reinforced with thin TPU skin', 'Knitted low-cut collar for snug ankle wrap', 'Dual-density TPU stud configuration for firm natural and artificial grass'],
                'tech_specs': {'Soleplate': 'Speedplate TPU', 'Studs': 'Bladed FG/AG', 'Weight': '210g'},
                'primary_image': 'https://images.unsplash.com/photo-1511886929837-354d827aae26?w=800&auto=format&fit=crop&q=80',
                'secondary_image': 'https://images.unsplash.com/photo-1575361204480-aadea25e6e68?w=800&auto=format&fit=crop&q=80',
                'available_sizes': ['UK 6', 'UK 7', 'UK 8', 'UK 9', 'UK 10', 'UK 11'],
                'colors': ['Electric Orange / Metallic Navy', 'Blackout Stealth'],
                'in_stock': True,
                'is_featured': True
            },
            {
                'name': 'AMS Striker Pro FIFA Match Football',
                'slug': 'ams-striker-pro-fifa-match-ball',
                'category': cat_map['football'],
                'sport': 'Football',
                'gender': 'UNISEX',
                'price': 2499.00,
                'original_price': 3499.00,
                'badge': 'FIFA QUALITY',
                'rating': 4.8,
                'reviews_count': 93,
                'description': 'Thermally-bonded seamless 32-panel FIFA Quality Pro certified match ball. Delivers true aerodynamic flight trajectory and zero water absorption in heavy monsoon play.',
                'features': ['Thermal bonding technology creates seamless surface', 'Textured PU outer skin for optimal touch in wet conditions', 'High-rebound butyl bladder for sustained air pressure', 'Precision laser aerodynamic grooving'],
                'tech_specs': {'Size': 'Official Size 5', 'Construction': 'Thermally Bonded 32 Panels', 'Certification': 'FIFA Quality Pro Equivalent'},
                'primary_image': 'https://images.unsplash.com/photo-1614632537423-1e6c2e7e0aab?w=800&auto=format&fit=crop&q=80',
                'secondary_image': 'https://images.unsplash.com/photo-1511886929837-354d827aae26?w=800&auto=format&fit=crop&q=80',
                'available_sizes': ['Size 5 Match', 'Size 4 Youth'],
                'colors': ['White / Neon Cyber Yellow / Red', 'Hyper Blue'],
                'in_stock': True,
                'is_featured': False
            },

            # Gym & Training
            {
                'name': 'AMS Fuse Apex Multi-Sport Training Shoes',
                'slug': 'ams-fuse-apex-training-shoes',
                'category': cat_map['training'],
                'sport': 'Fitness',
                'gender': 'MEN',
                'price': 5999.00,
                'original_price': 7999.00,
                'badge': 'CROSSFIT READY',
                'rating': 4.7,
                'reviews_count': 78,
                'description': 'Engineered in collaboration with elite athletes for high-intensity interval training, heavy barbell squats, and explosive box jumps. Features 4mm low drop and flared heel stability wrap.',
                'features': ['Wide toe box for maximum foot splay during deadlifts', 'High-abrasion resistant ballistic mesh', 'Vertical flex grooves for sprint transitions', 'PUMAGRIP rubber wraps up the midsole for rope climbs'],
                'tech_specs': {'Drop': '4mm Flat Platform', 'Weight': '310g', 'Outsole': 'High-Grip Rubber Wall'},
                'primary_image': 'https://images.unsplash.com/photo-1584735935682-2f2b69dff9d2?w=800&auto=format&fit=crop&q=80',
                'secondary_image': 'https://images.unsplash.com/photo-1595950653106-6c9ebd614d3a?w=800&auto=format&fit=crop&q=80',
                'available_sizes': ['UK 7', 'UK 8', 'UK 9', 'UK 10', 'UK 11'],
                'colors': ['Matte Black / Charcoal Silver', 'Crimson Pulse'],
                'in_stock': True,
                'is_featured': True
            },
            {
                'name': 'AMS DryCell Compression Training Tracksuit',
                'slug': 'ams-drycell-compression-tracksuit',
                'category': cat_map['training'],
                'sport': 'Fitness',
                'gender': 'MEN',
                'price': 3999.00,
                'original_price': 5999.00,
                'badge': 'POPULAR',
                'rating': 4.8,
                'reviews_count': 130,
                'description': 'Complete athletic performance tracksuit featuring moisture-wicking full-zip jacket and tapered athletic joggers with secure zippered device pockets.',
                'features': ['4-way stretch poly-elastane double knit fabric', 'Ergonomic raglan sleeves for unrestricted arm movement', 'Elasticated waistband with interior silicone grip drawcord', 'Ankle zips for easy on/off over training shoes'],
                'tech_specs': {'Material': '90% Recycled Polyester, 10% Spandex', 'Fit': 'Tapered Athletic Fit', 'Pockets': '3 Zip Pockets'},
                'primary_image': 'https://images.unsplash.com/photo-1556906781-9a412961c28c?w=800&auto=format&fit=crop&q=80',
                'secondary_image': 'https://images.unsplash.com/photo-1517838277536-f5f99be501cd?w=800&auto=format&fit=crop&q=80',
                'available_sizes': ['S', 'M', 'L', 'XL', 'XXL'],
                'colors': ['Stealth Black / Volt Accents', 'Deep Navy / Silver'],
                'in_stock': True,
                'is_featured': False
            },
            {
                'name': 'AMS Heavy Duty 45L Tactical Gym Duffle',
                'slug': 'ams-heavy-duty-gym-duffle',
                'category': cat_map['training'],
                'sport': 'Fitness',
                'gender': 'UNISEX',
                'price': 2299.00,
                'original_price': 3499.00,
                'badge': 'WATER RESISTANT',
                'rating': 4.9,
                'reviews_count': 64,
                'description': 'Weather-resistant 900D ballistic cordura duffle featuring a separate ventilated dirty shoe tunnel, waterproof wet gear pocket, and cushioned ergonomic shoulder strap.',
                'features': ['Isolated ventilated shoe compartment fits up to UK 13 shoes', 'Waterproof TPU-lined wet towel compartment', 'Padded laptop sleeve (up to 16 inches)', 'Heavy duty YKK weather-sealed zippers'],
                'tech_specs': {'Capacity': '45 Liters', 'Dimensions': '54cm x 28cm x 28cm', 'Fabric': '900D Ballistic Cordura'},
                'primary_image': 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=800&auto=format&fit=crop&q=80',
                'secondary_image': 'https://images.unsplash.com/photo-1517838277536-f5f99be501cd?w=800&auto=format&fit=crop&q=80',
                'available_sizes': ['45L Standard'],
                'colors': ['Midnight Carbon / Neon Red Pulls', 'Military Olive'],
                'in_stock': True,
                'is_featured': False
            },

            # Badminton
            {
                'name': 'AMS Volt Carbon 100 Badminton Racquet',
                'slug': 'ams-volt-carbon-100-badminton-racquet',
                'category': cat_map['badminton'],
                'sport': 'Badminton',
                'gender': 'UNISEX',
                'price': 4499.00,
                'original_price': 6999.00,
                'badge': 'SMASH POWER',
                'rating': 4.9,
                'reviews_count': 82,
                'description': 'Head-heavy badminton weapon constructed from Japanese Toray 40T high modulus graphite. Provides explosive smash velocity and hyper-accurate drops at the net.',
                'features': ['Toray 40T Nano Carbon graphite shaft', 'Isometric aerodynamic aero-box head frame', 'Pre-strung at 28 lbs with high tension multi-filament gut', 'Anti-torsion slim cap for rapid wrist maneuvers'],
                'tech_specs': {'Weight': '4U (82g +/- 2g)', 'Balance': 'Head Heavy (300mm)', 'Tension': 'Up to 32 LBS', 'Flex': 'Medium Stiff'},
                'primary_image': 'https://images.unsplash.com/photo-1626224583764-f87db24ac4ea?w=800&auto=format&fit=crop&q=80',
                'secondary_image': 'https://images.unsplash.com/photo-1613918108466-292b78a8ef95?w=800&auto=format&fit=crop&q=80',
                'available_sizes': ['G4 Grip', 'G5 Grip'],
                'colors': ['Matte Black / Flame Red', 'Electric Blue'],
                'in_stock': True,
                'is_featured': True
            },
            {
                'name': 'AMS Tour Feather Shuttles (Tube of 12)',
                'slug': 'ams-tour-feather-shuttles-tube',
                'category': cat_map['badminton'],
                'sport': 'Badminton',
                'gender': 'UNISEX',
                'price': 1699.00,
                'original_price': 2199.00,
                'badge': 'TOURNAMENT GRADE',
                'rating': 4.6,
                'reviews_count': 51,
                'description': 'Selected goose feather tournament shuttlecocks with natural sandwich cork base for rock-solid flight stability, pinpoint trajectory, and extended smash durability.',
                'features': ['100% Grade A Selected goose feathers', 'Solid two-piece natural wood cork base', 'Consistent flight speed (Speed 77 / 78)', 'Tested for recovery trajectory after hard smashes'],
                'tech_specs': {'Speed': 'Speed 77 (Medium)', 'Quantity': '12 Shuttles per Tube', 'Base': 'Natural Cork'},
                'primary_image': 'https://images.unsplash.com/photo-1613918108466-292b78a8ef95?w=800&auto=format&fit=crop&q=80',
                'secondary_image': 'https://images.unsplash.com/photo-1626224583764-f87db24ac4ea?w=800&auto=format&fit=crop&q=80',
                'available_sizes': ['Standard Tube (12 Shuttles)'],
                'colors': ['Pure White'],
                'in_stock': True,
                'is_featured': False
            },

            # Motorsport & Lifestyle
            {
                'name': 'AMS Scuderia Turbo Track Jacket',
                'slug': 'ams-scuderia-turbo-track-jacket',
                'category': cat_map['lifestyle'],
                'sport': 'Motorsport',
                'gender': 'UNISEX',
                'price': 4999.00,
                'original_price': 7499.00,
                'badge': 'MOTORSPORT DROP',
                'rating': 4.8,
                'reviews_count': 95,
                'description': 'Inspired by championship racing paddock culture. Features aggressive color-blocking, contrast racing stripes down the sleeves, and high-density rubberized chest crest.',
                'features': ['Contrast chevron speed inserts', 'Ribbed cuffs and race collar', 'Branded dual-slider metal zipper pull', 'Breathable mesh interior lining'],
                'tech_specs': ['Material: 100% Recycled Poly-Twill', 'Fit: Regular Athletic', 'Style: Iconic Motorsport T7'],
                'primary_image': 'https://images.unsplash.com/photo-1552346154-21d32810aba3?w=800&auto=format&fit=crop&q=80',
                'secondary_image': 'https://images.unsplash.com/photo-1556906781-9a412961c28c?w=800&auto=format&fit=crop&q=80',
                'available_sizes': ['S', 'M', 'L', 'XL', 'XXL'],
                'colors': ['Puma Red / Motorsport White / Black', 'Triple Black'],
                'in_stock': True,
                'is_featured': True
            },
            {
                'name': 'AMS Slipstream Heritage Court Sneakers',
                'slug': 'ams-slipstream-heritage-court',
                'category': cat_map['lifestyle'],
                'sport': 'Lifestyle',
                'gender': 'UNISEX',
                'price': 6999.00,
                'original_price': 9999.00,
                'badge': 'HERITAGE DROP',
                'rating': 4.9,
                'reviews_count': 120,
                'description': 'Born in the 80s as a basketball powerhouse, reimagined today as an iconic streetwear classic with premium leather overlays and vintage off-white rubber cupsole.',
                'features': ['Full-grain leather and suede upper overlays', 'Perforated toe box for retro basketball heritage', 'Cushioned ankle collar and tongue', 'Durable non-marking cupsole rubber traction'],
                'tech_specs': {'Upper': 'Leather & Suede', 'Sole': 'Rubber Cupsole', 'Style': 'Low-top Court Classic'},
                'primary_image': 'https://images.unsplash.com/photo-1552346154-21d32810aba3?w=800&auto=format&fit=crop&q=80',
                'secondary_image': 'https://images.unsplash.com/photo-1608231387042-66d1773070a5?w=800&auto=format&fit=crop&q=80',
                'available_sizes': ['UK 6', 'UK 7', 'UK 8', 'UK 9', 'UK 10', 'UK 11'],
                'colors': ['Vintage White / Racing Green', 'Chalk / Black'],
                'in_stock': True,
                'is_featured': True
            }
        ]

        for pdata in products_data:
            Product.objects.create(**pdata)

        self.stdout.write(self.style.SUCCESS(f"Successfully seeded {Category.objects.count()} categories and {Product.objects.count()} products for Anand Mangal Sports!"))
