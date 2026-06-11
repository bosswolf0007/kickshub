/**
 * KicksHub Mock API Seed Script
 * 
 * HOW TO USE:
 * 1. Open your website in browser (http://localhost:5173)
 * 2. Open Developer Console (F12 > Console)
 * 3. Copy-paste the ENTIRE content of this file
 * 4. Press Enter
 * 5. Refresh the page (F5)
 * 6. All data will appear!
 * 
 * This seeds ALL data into localStorage for the Mock API.
 */

(function() {
  console.log('🌱 KicksHub - Seeding Mock API Data...');
  
  // ================================================================
  // USERS
  // ================================================================
  const users = [
    { id: 1, full_name: 'Admin KicksHub', business_name: 'KicksHub Wholesale Pvt Ltd', email: 'admin@kickshub.in', phone: '9876543210', password_hash: 'admin123', gst_number: '27ABCDE1234F1Z5', address: '123, Footwear Market, BKC Complex', city: 'Mumbai', state: 'Maharashtra', pincode: '400051', role: 'admin', status: 'approved' },
    { id: 2, full_name: 'Rajesh Kumar', business_name: 'Kicks Footwear Store', email: 'rajesh@kicksfootwear.in', phone: '9876543211', password_hash: 'dealer123', gst_number: '07FGHI5678J2K6', address: '45, Shoe Market, Chandni Chowk', city: 'Delhi', state: 'Delhi', pincode: '110006', role: 'dealer', status: 'approved' },
    { id: 3, full_name: 'Priya Sharma', business_name: 'Stepso Footwear', email: 'priya@stepso.in', phone: '9876543212', password_hash: 'dealer123', gst_number: '27JKLM9012N3P7', address: '78, Fashion Street, Colaba', city: 'Mumbai', state: 'Maharashtra', pincode: '400005', role: 'dealer', status: 'approved' },
    { id: 4, full_name: 'Amit Patel', business_name: 'Hommy Spot', email: 'amit@hammyspot.in', phone: '9876543213', password_hash: 'dealer123', gst_number: '24QRST3456U7V8', address: '12, CG Road', city: 'Ahmedabad', state: 'Gujarat', pincode: '380009', role: 'dealer', status: 'approved' },
    { id: 5, full_name: 'Sneha Reddy', business_name: 'Reddy Footwear World', email: 'sneha@reddyfw.in', phone: '9876543214', password_hash: 'dealer123', gst_number: '36WXYZ7890A1B2', address: '56, RB Road, Secunderabad', city: 'Hyderabad', state: 'Telangana', pincode: '500003', role: 'dealer', status: 'approved' },
    { id: 6, full_name: 'Vikram Singh', business_name: 'Singh Shoes & Sons', email: 'vikram@singhshoes.in', phone: '9876543215', password_hash: 'dealer123', gst_number: '09CDEF3456G7H8', address: '23, MI Road', city: 'Jaipur', state: 'Rajasthan', pincode: '302001', role: 'dealer', status: 'approved' },
    { id: 7, full_name: 'Ananya Gupta', business_name: 'Gupta Footwear Bazaar', email: 'ananya@guptafw.in', phone: '9876543216', password_hash: 'dealer123', gst_number: '09IJKL7890M1N2', address: '89, Nai Sarak', city: 'Lucknow', state: 'Uttar Pradesh', pincode: '226001', role: 'dealer', status: 'pending' },
    { id: 8, full_name: 'Rahul Verma', business_name: 'Verma Shoe Palace', email: 'rahul@vermasp.in', phone: '9876543217', password_hash: 'dealer123', gst_number: '', address: '34, MG Road, Camp', city: 'Pune', state: 'Maharashtra', pincode: '411001', role: 'dealer', status: 'approved' },
    { id: 9, full_name: 'Deepika Joshi', business_name: 'Joshi Footwear Hub', email: 'deepika@joshifh.in', phone: '9876543218', password_hash: 'dealer123', gst_number: '29OPQR1234S5T6', address: '67, Commercial Street', city: 'Bengaluru', state: 'Karnataka', pincode: '560001', role: 'dealer', status: 'approved' },
    { id: 10, full_name: 'Karan Malhotra', business_name: 'Malhotra Shoe Company', email: 'karan@malhotrashoe.in', phone: '9876543221', password_hash: 'dealer123', gst_number: '03ABCD9012E3F4', address: '56, Sector 17', city: 'Chandigarh', state: 'Chandigarh', pincode: '160017', role: 'dealer', status: 'blocked' },
    { id: 11, full_name: 'Ravi Shankar', business_name: 'Shankar Wholesale Shoes', email: 'ravi@shankarws.in', phone: '9876543223', password_hash: 'dealer123', gst_number: '33CDEF7890G1H2', address: '45, Ranganathan Street', city: 'Chennai', state: 'Tamil Nadu', pincode: '600001', role: 'dealer', status: 'approved' },
  ];
  
  // ================================================================
  // COLORS
  // ================================================================
  const colors = [
    { id: 1, name: 'Black', hex_code: '#000000' },
    { id: 2, name: 'White', hex_code: '#FFFFFF' },
    { id: 3, name: 'Brown', hex_code: '#8B4513' },
    { id: 4, name: 'Blue', hex_code: '#0000FF' },
    { id: 5, name: 'Red', hex_code: '#FF0000' },
    { id: 6, name: 'Green', hex_code: '#008000' },
    { id: 7, name: 'Grey', hex_code: '#808080' },
    { id: 8, name: 'Navy', hex_code: '#000080' },
    { id: 9, name: 'Pink', hex_code: '#FFC0CB' },
    { id: 10, name: 'Purple', hex_code: '#800080' },
    { id: 12, name: 'Beige', hex_code: '#F5F5DC' },
    { id: 19, name: 'Charcoal', hex_code: '#36454F' },
    { id: 20, name: 'Cream', hex_code: '#FFFDD0' },
    { id: 21, name: 'Khaki', hex_code: '#C3B091' },
    { id: 22, name: 'Sky Blue', hex_code: '#87CEEB' },
  ];
  
  // ================================================================
  // SIZES
  // ================================================================
  const sizes = [
    { id: 1, name: '1' }, { id: 2, name: '2' }, { id: 3, name: '3' },
    { id: 4, name: '4' }, { id: 5, name: '5' }, { id: 6, name: '6' },
    { id: 7, name: '7' }, { id: 8, name: '8' }, { id: 9, name: '9' },
    { id: 10, name: '10' }, { id: 11, name: '11' }, { id: 12, name: '12' },
    { id: 13, name: '13' }, { id: 14, name: '14' },
    { id: 17, name: 'S' }, { id: 18, name: 'M' }, { id: 19, name: 'L' },
    { id: 20, name: 'XL' }, { id: 21, name: 'XXL' },
  ];
  
  // ================================================================
  // PRODUCTS (70+ products with full data)
  // ================================================================
  const productDefs = [
    // School Shoes (cat 1)
    { cat: 1, name: 'Premium School Shoe - Black', desc: 'High-quality school shoe in premium black leather. Durable sole, reinforced stitching, comfortable insole.', price: 450, compare: 599, brand: 'KicksHub Premium', colors: [1,2], sizes: [6,7,8,9,10,11,12], stock: 500, moq: 10, disc: 25, feat: 1 },
    { cat: 1, name: 'School Oxford Shoe - White', desc: 'Classic white school oxford made from premium synthetic leather. Lightweight, breathable.', price: 425, compare: 575, brand: 'KicksHub Premium', colors: [2], sizes: [6,7,8,9,10,11], stock: 350, moq: 10, disc: 26, feat: 1 },
    { cat: 1, name: 'Junior School Sneakers', desc: 'Comfortable sneakers for junior students. Soft cushion, breathable mesh, velcro closure.', price: 380, compare: 499, brand: 'KicksHub Value', colors: [1,4,2], sizes: [5,6,7,8,9], stock: 400, moq: 10, disc: 24, feat: 0 },
    { cat: 1, name: 'School Formal Shoes - Brown', desc: 'Premium brown formal school shoes with durable leather finish. Anti-skid sole.', price: 475, compare: 649, brand: 'KicksHub Premium', colors: [3,1], sizes: [7,8,9,10,11,12], stock: 250, moq: 10, disc: 27, feat: 0 },
    { cat: 1, name: 'School Loafers - Navy Blue', desc: 'Smart navy blue loafers with slip-on design. Premium synthetic upper.', price: 400, compare: 549, brand: 'Action', colors: [8,1], sizes: [6,7,8,9,10], stock: 200, moq: 10, disc: 25, feat: 0 },
    { cat: 1, name: 'School Sports Shoes - White/Blue', desc: 'Multi-purpose sports shoes for PT and daily wear. Lightweight EVA sole.', price: 520, compare: 699, brand: 'KicksHub Value', colors: [2,4], sizes: [6,7,8,9,10,11], stock: 300, moq: 10, disc: 26, feat: 0 },
    
    // Men's (cat 2)
    { cat: 2, name: "Men's Formal Derby - Black", desc: 'Premium black derby shoes. Genuine leather, classic design for office and formal occasions.', price: 1299, compare: 1799, brand: 'Liberty', colors: [1], sizes: [7,8,9,10,11,12], stock: 200, moq: 6, disc: 28, feat: 1 },
    { cat: 2, name: "Men's Casual Loafers - Brown", desc: 'Stylish brown casual loafers. Premium synthetic leather, cushioned insole.', price: 899, compare: 1299, brand: 'Paragon', colors: [3,1,12], sizes: [7,8,9,10,11], stock: 300, moq: 6, disc: 30, feat: 1 },
    { cat: 2, name: "Men's Sports Running Shoes", desc: 'High-performance running shoes. Breathable mesh, shock-absorbing sole.', price: 1499, compare: 1999, brand: 'KicksHub Premium', colors: [1,4,5], sizes: [7,8,9,10,11,12], stock: 250, moq: 6, disc: 25, feat: 1 },
    { cat: 2, name: "Men's Sneakers - White", desc: 'Trendy white sneakers. Padded collar, rubber outsole. Perfect for daily wear.', price: 1099, compare: 1499, brand: 'KicksHub Premium', colors: [2,1,7], sizes: [7,8,9,10,11], stock: 400, moq: 6, disc: 27, feat: 1 },
    { cat: 2, name: "Men's Leather Boots - Brown", desc: 'Rugged brown leather boots. Premium leather, sturdy sole, metal eyelets.', price: 1899, compare: 2499, brand: 'Bata India', colors: [3,1], sizes: [8,9,10,11,12], stock: 150, moq: 6, disc: 24, feat: 0 },
    { cat: 2, name: "Men's Formal Oxford - Black Patent", desc: 'Premium black patent leather oxford. High-gloss finish. Perfect for weddings.', price: 1599, compare: 2199, brand: 'Liberty', colors: [1], sizes: [8,9,10,11], stock: 120, moq: 6, disc: 27, feat: 0 },
    
    // Women's (cat 3)
    { cat: 3, name: "Women's Heeled Sandals - Black", desc: 'Elegant black heeled sandals. Block heel, adjustable strap for parties.', price: 899, compare: 1299, brand: 'KicksHub Premium', colors: [1,19], sizes: [5,6,7,8,9], stock: 250, moq: 6, disc: 30, feat: 1 },
    { cat: 3, name: "Women's Casual Flats - Ballet", desc: 'Comfortable ballet flats. Soft upper, padded insole for everyday wear.', price: 599, compare: 849, brand: 'KicksHub Premium', colors: [1,2,10,5], sizes: [5,6,7,8,9], stock: 400, moq: 6, disc: 29, feat: 1 },
    { cat: 3, name: "Women's Sneakers - White", desc: 'Chunky sole white sneakers. Padded collar, breathable lining. Trendy style!', price: 1099, compare: 1499, brand: 'KicksHub Premium', colors: [2,20,21], sizes: [5,6,7,8,9,10], stock: 300, moq: 6, disc: 25, feat: 1 },
    { cat: 3, name: "Women's Party Heels - Gold", desc: 'Stunning gold party heels with embellished design for festive occasions.', price: 1299, compare: 1799, brand: 'KicksHub Premium', colors: [22,1,2], sizes: [5,6,7,8,9], stock: 150, moq: 6, disc: 28, feat: 0 },
    { cat: 3, name: "Women's Wedge Sandals - Beige", desc: 'Comfortable wedge sandals with braided detail. Perfect for summer.', price: 799, compare: 1099, brand: 'Relaxo', colors: [12,3], sizes: [5,6,7,8,9], stock: 280, moq: 6, disc: 27, feat: 0 },
    { cat: 3, name: "Women's Ankle Boots", desc: 'Stylish ankle boots. Side zipper, block heel for winter and monsoon.', price: 1499, compare: 1999, brand: 'KicksHub Premium', colors: [1,3,19], sizes: [6,7,8,9,10], stock: 180, moq: 6, disc: 25, feat: 0 },
    
    // Kids (cat 4)
    { cat: 4, name: "Kids' Running Shoes - Blue", desc: 'Fun blue running shoes. Lightweight, flexible sole for active kids.', price: 599, compare: 849, brand: 'KicksHub Value', colors: [4,1,5], sizes: [1,2,3,4,5,6], stock: 350, moq: 12, disc: 25, feat: 1 },
    { cat: 4, name: "Baby Soft Sole - First Walkers", desc: 'Soft sole shoes for babies learning to walk. Cotton upper, suede sole.', price: 349, compare: 499, brand: 'KicksHub Premium', colors: [2,9,22], sizes: [1,2,3], stock: 400, moq: 12, disc: 20, feat: 1 },
    { cat: 4, name: "Kids' Casual Sneakers", desc: 'Colorful sneakers with fun designs. Easy velcro straps for quick wear.', price: 499, compare: 699, brand: 'KicksHub Value', colors: [4,5,2,1], sizes: [2,3,4,5,6], stock: 450, moq: 12, disc: 22, feat: 1 },
    { cat: 4, name: "Kids' Sandals", desc: 'Durable sandals with adjustable straps. Protective toe cap for outdoor play.', price: 399, compare: 549, brand: 'Paragon', colors: [4,5,7], sizes: [2,3,4,5,6], stock: 300, moq: 12, disc: 24, feat: 0 },
    { cat: 4, name: "Kids' Party Shoes - Formal", desc: 'Smart formal shoes for special occasions. Patent finish with buckle.', price: 699, compare: 949, brand: 'Liberty', colors: [1,2], sizes: [3,4,5,6], stock: 200, moq: 12, disc: 25, feat: 0 },
    { cat: 4, name: "Kids' Rain Boots", desc: 'Waterproof boots with warm lining. Non-slip sole. Fun colors!', price: 799, compare: 1099, brand: 'KicksHub Premium', colors: [5,4,1], sizes: [3,4,5,6,7], stock: 150, moq: 12, disc: 22, feat: 0 },
    
    // Socks (cat 5)
    { cat: 5, name: 'Ankle Socks - Cotton Pack of 6', desc: 'Breathable cotton ankle socks. Reinforced heel/toe. Pack of 6 pairs.', price: 199, compare: 299, brand: 'KicksHub Premium', colors: [1,2,7,4], sizes: [17,18,19,20], stock: 1000, moq: 24, disc: 33, feat: 1 },
    { cat: 5, name: 'Crew Socks - Formal Black Pack of 3', desc: 'Premium formal crew socks. Cotton blend. Perfect for office. Pack of 3.', price: 249, compare: 349, brand: 'KicksHub Premium', colors: [1,19], sizes: [18,19,20], stock: 800, moq: 24, disc: 30, feat: 1 },
    { cat: 5, name: 'Knee High Socks - School White Pack of 3', desc: 'School knee-high socks. Durable cotton-polyester. Approved for schools.', price: 299, compare: 399, brand: 'KicksHub Premium', colors: [2], sizes: [1,2,3,4,5,6,17,18,19], stock: 600, moq: 24, disc: 28, feat: 1 },
    { cat: 5, name: 'No-Show Socks - Invisible Pack of 5', desc: 'Invisible socks with silicone heel grip. Ultra-thin design. Pack of 5.', price: 249, compare: 349, brand: 'KicksHub Premium', colors: [1,2,4,7], sizes: [17,18,19,20], stock: 700, moq: 24, disc: 29, feat: 0 },
    { cat: 5, name: 'Sports Socks - Cushioned Pack of 3', desc: 'Performance sports socks. Moisture-wicking fabric with arch support.', price: 349, compare: 499, brand: 'KicksHub Premium', colors: [2,1,4], sizes: [18,19,20,21], stock: 500, moq: 24, disc: 30, feat: 0 },
    { cat: 5, name: 'Wool Winter Socks - Pack of 2', desc: 'Warm wool blend winter socks. Thermal comfort for cold weather.', price: 399, compare: 549, brand: 'KicksHub Premium', colors: [1,7,3], sizes: [18,19,20], stock: 300, moq: 12, disc: 25, feat: 0 },
    
    // Accessories (cat 6)
    { cat: 6, name: 'Shoe Polish Kit - Complete Care', desc: 'Complete kit with black, brown, neutral polish. Includes brush and cloth.', price: 199, compare: 299, brand: 'KicksHub Premium', colors: [], sizes: [21], stock: 500, moq: 12, disc: 20, feat: 1 },
    { cat: 6, name: 'Shoe Laces Premium Pack - 6 Pairs', desc: 'Premium laces pack. Assorted colors. 120cm length. Durable polyester.', price: 99, compare: 149, brand: 'KicksHub Premium', colors: [1,2,3,8], sizes: [21], stock: 1000, moq: 24, disc: 34, feat: 1 },
    { cat: 6, name: 'Memory Foam Insoles - Comfort Plus', desc: 'Premium memory foam insoles. Shock-absorbing, arch support. Trimmable.', price: 299, compare: 449, brand: 'KicksHub Premium', colors: [1,2], sizes: [17,18,19,20], stock: 600, moq: 12, disc: 25, feat: 1 },
    { cat: 6, name: 'Shoe Deodorizer Spray - 200ml', desc: 'Eliminates odor-causing bacteria. Long-lasting fresh fragrance. 200ml.', price: 149, compare: 199, brand: 'KicksHub Premium', colors: [], sizes: [21], stock: 400, moq: 12, disc: 25, feat: 0 },
    { cat: 6, name: 'Shoe Bags - Travel Pack of 3', desc: 'Waterproof nylon shoe bags for travel. Drawstring closure. Pack of 3.', price: 249, compare: 349, brand: 'KicksHub Premium', colors: [1,4,7], sizes: [21], stock: 350, moq: 12, disc: 28, feat: 0 },
    
    // EVA (cat 7)
    { cat: 7, name: 'EVA Slides - Classic Black', desc: 'Ultra-lightweight, waterproof EVA slides. Cushioned footbed with massage dots.', price: 249, compare: 399, brand: 'KicksHub Premium', colors: [1,4,5], sizes: [6,7,8,9,10,11,12,13], stock: 800, moq: 12, disc: 35, feat: 1 },
    { cat: 7, name: 'EVA Sandals - Comfort Fit', desc: 'Lightweight, flexible, waterproof EVA sandals. Adjustable strap.', price: 299, compare: 449, brand: 'KicksHub Value', colors: [1,2,4,9], sizes: [7,8,9,10,11,12], stock: 600, moq: 12, disc: 32, feat: 1 },
    { cat: 7, name: 'Premium EVA Flip Flops', desc: 'Soft cushioned sole, durable strap. Available in multiple colors.', price: 199, compare: 299, brand: 'KicksHub Premium', colors: [1,2,4,5,8], sizes: [7,8,9,10,11,12,13], stock: 900, moq: 12, disc: 40, feat: 1 },
    { cat: 7, name: 'EVA Bathroom Slippers - Anti-Skid', desc: 'Drainage holes, quick-drying, mold-resistant with textured grip sole.', price: 179, compare: 249, brand: 'KicksHub Value', colors: [1,2,22,9], sizes: [7,8,9,10,11], stock: 1000, moq: 12, disc: 38, feat: 0 },
    { cat: 7, name: 'Memory Foam EVA Slides - Luxury', desc: 'Memory foam footbed for ultimate comfort. Thick cushioned sole.', price: 449, compare: 649, brand: 'KicksHub Premium', colors: [1,2,7,8], sizes: [7,8,9,10,11,12], stock: 400, moq: 12, disc: 25, feat: 0 },
    
    // PU (cat 8)
    { cat: 8, name: 'PU Formal Shoes - Black', desc: 'Professional black PU formal shoes. Padded insole, durable construction.', price: 799, compare: 1099, brand: 'KicksHub Premium', colors: [1], sizes: [7,8,9,10,11,12], stock: 400, moq: 6, disc: 28, feat: 1 },
    { cat: 8, name: 'PU Loafers - Brown', desc: 'Stylish brown PU loafers with tassel detail. Easy slip-on design.', price: 699, compare: 949, brand: 'KicksHub Value', colors: [3,1], sizes: [7,8,9,10,11], stock: 350, moq: 6, disc: 27, feat: 1 },
    { cat: 8, name: 'PU Sneakers - White', desc: 'Trendy white PU sneakers with perforations. Breathable and comfortable.', price: 599, compare: 849, brand: 'KicksHub Premium', colors: [2,1,4], sizes: [7,8,9,10,11,12], stock: 500, moq: 6, disc: 30, feat: 1 },
    { cat: 8, name: "Women's PU Sandals", desc: 'Adjustable strap, cushioned footbed, lightweight design for daily wear.', price: 449, compare: 649, brand: 'KicksHub Premium', colors: [1,2,12,9], sizes: [5,6,7,8,9], stock: 450, moq: 6, disc: 29, feat: 0 },
    { cat: 8, name: 'PU Ankle Boots', desc: 'Side zipper, faux leather finish, comfortable block heel.', price: 999, compare: 1399, brand: 'KicksHub Premium', colors: [1,3,19], sizes: [7,8,9,10,11], stock: 200, moq: 6, disc: 25, feat: 0 },
    
    // Hawai (cat 9)
    { cat: 9, name: 'Classic Hawai Chappal - Black', desc: 'Original classic Hawai chappal. Durable rubber, iconic design. Bulk pack available.', price: 149, compare: 199, brand: 'Paragon', colors: [1,2], sizes: [7,8,9,10,11,12,13], stock: 2000, moq: 24, disc: 40, feat: 1 },
    { cat: 9, name: 'Premium Hawai - Cushioned', desc: 'Extra cushioned footbed for enhanced comfort. Durable rubber sole.', price: 199, compare: 299, brand: 'Paragon', colors: [1,2,4,5,8], sizes: [7,8,9,10,11,12,13], stock: 1500, moq: 24, disc: 35, feat: 1 },
    { cat: 9, name: 'Designer Hawai Chappal', desc: 'Printed straps with colorful patterns. Same durable rubber sole. Stand out!', price: 249, compare: 349, brand: 'KicksHub Premium', colors: [4,5,9,22], sizes: [7,8,9,10,11,12], stock: 800, moq: 24, disc: 30, feat: 0 },
    { cat: 9, name: "Women's Slim Fit Hawai", desc: 'Slim-fit design with narrower strap. Lightweight and stylish.', price: 149, compare: 199, brand: 'Paragon', colors: [9,5,2,1], sizes: [5,6,7,8,9], stock: 1000, moq: 24, disc: 33, feat: 0 },
    { cat: 9, name: "Kids' Fun Hawai", desc: 'Fun character prints on soft rubber. Perfect for kids!', price: 99, compare: 149, brand: 'Paragon', colors: [5,4,9,22], sizes: [1,2,3,4,5,6], stock: 1200, moq: 24, disc: 40, feat: 0 },
    
    // Imported (cat 10)
    { cat: 10, name: 'Premium Running Shoes - Imported', desc: 'Advanced cushioning technology. Lightweight mesh. International quality.', price: 2499, compare: 3499, brand: "Adidas (Import)", colors: [1,4,5], sizes: [7,8,9,10,11,12], stock: 100, moq: 6, disc: 20, feat: 1 },
    { cat: 10, name: 'Imported Lifestyle Sneakers', desc: 'Premium materials with superior comfort. International brand design.', price: 1999, compare: 2999, brand: "Puma (Import)", colors: [2,1,4,5], sizes: [7,8,9,10,11], stock: 120, moq: 6, disc: 18, feat: 1 },
    { cat: 10, name: 'Imported Leather Boots', desc: 'Full-grain leather with premium construction. Built to last.', price: 3999, compare: 5499, brand: "Nike (Import)", colors: [3,1], sizes: [8,9,10,11,12], stock: 50, moq: 6, disc: 15, feat: 1 },
    { cat: 10, name: 'Imported Training Shoes', desc: 'Professional gym training shoes with excellent grip and support.', price: 2199, compare: 2999, brand: "Nike (Import)", colors: [1,4,5,7], sizes: [7,8,9,10,11,12], stock: 80, moq: 6, disc: 17, feat: 0 },
    { cat: 10, name: 'Imported Casual Slip-Ons', desc: 'Elastic panels for easy wear. Memory foam insole. Sleek design.', price: 1799, compare: 2499, brand: "Puma (Import)", colors: [1,2,8], sizes: [7,8,9,10,11], stock: 90, moq: 6, disc: 16, feat: 0 },
    
    // Branded (cat 11)
    { cat: 11, name: 'Campus Sneakers - Original', desc: 'Original Campus brand sneakers. Authorized distributor. Trendy design.', price: 899, compare: 1299, brand: 'KicksHub Value', colors: [2,1,4], sizes: [7,8,9,10,11], stock: 300, moq: 6, disc: 22, feat: 1 },
    { cat: 11, name: 'Bata Formal Shoes - Premium', desc: 'Genuine Bata formal shoes with quality guarantee. Classic styling.', price: 1399, compare: 1899, brand: 'Bata India', colors: [1,3], sizes: [7,8,9,10,11,12], stock: 200, moq: 6, disc: 20, feat: 1 },
    { cat: 11, name: 'Paragon Hawaii - Original', desc: 'Original Paragon Hawai chappal. Iconic quality trusted for generations.', price: 199, compare: 299, brand: 'Paragon', colors: [1,2,4,5], sizes: [7,8,9,10,11,12,13], stock: 2000, moq: 24, disc: 30, feat: 1 },
    { cat: 11, name: 'Relaxo Slippers - Comfort Plus', desc: 'Memory foam footbed. Lightweight EVA construction. Best-selling!', price: 349, compare: 499, brand: 'Relaxo', colors: [1,2,4], sizes: [7,8,9,10,11,12], stock: 600, moq: 12, disc: 25, feat: 0 },
    { cat: 11, name: 'Action Sports Shoes', desc: 'Breathable mesh upper with cushioned sole. Great value!', price: 799, compare: 1099, brand: 'Action', colors: [2,4,5], sizes: [7,8,9,10,11], stock: 350, moq: 6, disc: 24, feat: 0 },
    
    // Non-Branded (cat 12)
    { cat: 12, name: 'Economy Casual Shoes', desc: 'Affordable daily wear shoes. Durable construction, comfortable fit.', price: 349, compare: 499, brand: 'KicksHub Value', colors: [1,4,7], sizes: [7,8,9,10,11], stock: 600, moq: 12, disc: 30, feat: 1 },
    { cat: 12, name: 'Bulk Economy Slippers', desc: 'Mass market slippers at super affordable pricing. Bulk wholesale.', price: 99, compare: 149, brand: 'KicksHub Value', colors: [1,4,5], sizes: [7,8,9,10,11], stock: 2000, moq: 24, disc: 40, feat: 1 },
    { cat: 12, name: 'Budget School Shoes', desc: 'Price-sensitive option with essential quality. Ideal for tier-2 cities.', price: 299, compare: 399, brand: 'KicksHub Value', colors: [1,2], sizes: [6,7,8,9,10,11], stock: 800, moq: 12, disc: 28, feat: 0 },
    { cat: 12, name: 'Mass Market Chappal', desc: 'High-volume wholesale chappal. Basic design, super affordable. MOQ 50.', price: 79, compare: 129, brand: 'KicksHub Value', colors: [1,2], sizes: [7,8,9,10,11,12,13], stock: 5000, moq: 50, disc: 45, feat: 0 },
    { cat: 12, name: 'Economy Canvas Shoes', desc: 'Budget canvas shoes. Popular in rural and semi-urban markets.', price: 249, compare: 349, brand: 'KicksHub Value', colors: [1,4,7,8], sizes: [7,8,9,10,11], stock: 700, moq: 12, disc: 32, feat: 0 },
  ];
  
  // ================================================================
  // Build product objects
  // ================================================================
  const brandMap = { 'KicksHub Premium': 'KicksHub Premium', 'KicksHub Value': 'KicksHub Value', 'Bata India': 'Bata India', 'Paragon': 'Paragon', 'Relaxo': 'Relaxo', 'Liberty': 'Liberty', "Khadim's": "Khadim's", 'Action': 'Action', "Adidas (Import)": 'Adidas (Import)', "Nike (Import)": 'Nike (Import)', "Puma (Import)": 'Puma (Import)' };
  
  const catNames = {
    1: { name: 'School Shoes', slug: 'school-shoes' },
    2: { name: "Men's Collection", slug: 'mens' },
    3: { name: "Women's Collection", slug: 'womens' },
    4: { name: "Kids Collection", slug: 'kids' },
    5: { name: 'Socks', slug: 'socks' },
    6: { name: 'Accessories', slug: 'accessories' },
    7: { name: 'EVA Footwear', slug: 'eva' },
    8: { name: 'PU Footwear', slug: 'pu' },
    9: { name: 'Hawai Chappal', slug: 'hawai' },
    10: { name: 'Imported Collection', slug: 'imported' },
    11: { name: 'Branded Shoes', slug: 'branded' },
    12: { name: 'Non-Branded', slug: 'non-branded' },
  };
  
  const colorMap = {};
  colors.forEach(c => { colorMap[c.id] = { id: c.id, name: c.name, hex_code: c.hex_code }; });
  
  const sizeMap = {};
  sizes.forEach(s => { sizeMap[s.id] = { id: s.id, name: s.name }; });
  
  let products = [];
  let pid = 1;
  
  productDefs.forEach(def => {
    const cat = catNames[def.cat] || { name: 'General', slug: 'general' };
    const productColors = def.colors.map(cid => colorMap[cid]).filter(Boolean);
    const productSizes = def.sizes.map(sid => sizeMap[sid]).filter(Boolean);
    
    products.push({
      id: pid,
      name: def.name,
      description: def.desc,
      sku: `KH-${cat.slug.substring(0,3).toUpperCase()}-${String(pid).padStart(4, '0')}`,
      slug: def.name.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, ''),
      category_id: def.cat,
      category_name: cat.name,
      category_slug: cat.slug,
      brand_name: def.brand,
      price: def.price,
      compare_price: def.compare,
      stock: def.stock,
      moq: def.moq,
      discount: def.disc,
      is_featured: def.feat,
      is_active: 1,
      images: [],
      colors: productColors,
      sizes: productSizes,
      variants: [],
      created_at: new Date(Date.now() - Math.random() * 30 * 86400000).toISOString(),
    });
    pid++;
  });
  
  // ================================================================
  // INQUIRIES
  // ================================================================
  const inquiries = [
    { id: 1, user_id: 2, dealer_name: 'Rajesh Kumar', shop_name: 'Kicks Footwear Store', phone: '9876543211', gst_number: '07FGHI5678J2K6', address: '45, Shoe Market, Chandni Chowk', city: 'Delhi', state: 'Delhi', pincode: '110006', latitude: 28.7041, longitude: 77.1025, notes: 'Need this urgently for school season. Please confirm availability.', status: 'new', items_count: 3, items: [{ id: 1, product_id: 1, product_name: 'Premium School Shoe - Black', quantity: 50, size: '8', color: 'Black' }], created_at: new Date().toISOString() },
    { id: 2, user_id: 3, dealer_name: 'Priya Sharma', shop_name: 'Stepso Footwear', phone: '9876543212', gst_number: '27JKLM9012N3P7', address: '78, Fashion Street, Colaba', city: 'Mumbai', state: 'Maharashtra', pincode: '400005', latitude: 19.076, longitude: 72.8777, notes: 'Looking for bulk pricing on school shoes. Need 100 pairs.', status: 'contacted', items_count: 2, items: [{ id: 2, product_id: 2, product_name: 'School Oxford Shoe - White', quantity: 100, size: '7', color: 'White' }], created_at: new Date(Date.now() - 86400000).toISOString() },
    { id: 3, user_id: 4, dealer_name: 'Amit Patel', shop_name: 'Hommy Spot', phone: '9876543213', gst_number: '24QRST3456U7V8', address: '12, CG Road', city: 'Ahmedabad', state: 'Gujarat', pincode: '380009', latitude: 23.0225, longitude: 72.5714, notes: 'Need mixed sizes. Please confirm size-wise stock availability.', status: 'negotiation', items_count: 4, items: [{ id: 3, product_id: 7, product_name: "Men's Formal Derby - Black", quantity: 25, size: '9', color: 'Black' }], created_at: new Date(Date.now() - 2 * 86400000).toISOString() },
    { id: 4, user_id: 5, dealer_name: 'Sneha Reddy', shop_name: 'Reddy Footwear World', phone: '9876543214', gst_number: '36WXYZ7890A1B2', address: '56, RB Road, Secunderabad', city: 'Hyderabad', state: 'Telangana', pincode: '500003', latitude: 17.385, longitude: 78.4867, notes: 'Festival season stock needed. Delivery before Diwali please.', status: 'confirmed', items_count: 5, items: [{ id: 4, product_id: 13, product_name: "Women's Heeled Sandals - Black", quantity: 30, size: '7', color: 'Black' }], created_at: new Date(Date.now() - 5 * 86400000).toISOString() },
    { id: 5, user_id: 6, dealer_name: 'Vikram Singh', shop_name: 'Singh Shoes & Sons', phone: '9876543215', gst_number: '09CDEF3456G7H8', address: '23, MI Road', city: 'Jaipur', state: 'Rajasthan', pincode: '302001', latitude: 26.9124, longitude: 75.7873, notes: 'Regular monthly order. Same pricing as discussed.', status: 'closed', items_count: 2, items: [{ id: 5, product_id: 19, name: "Kids' Running Shoes - Blue", quantity: 200, size: '4', color: 'Blue' }], created_at: new Date(Date.now() - 10 * 86400000).toISOString() },
  ];
  
  // ================================================================
  // SAVE EVERYTHING TO LOCALSTORAGE
  // ================================================================
  localStorage.setItem('kickshub_mock_users', JSON.stringify(users));
  localStorage.setItem('kickshub_mock_products', JSON.stringify(products));
  localStorage.setItem('kickshub_mock_inquiries', JSON.stringify(inquiries));
  localStorage.setItem('kickshub_mock_seeded', 'true');
  
  console.log(`✅ Seeded successfully!
  📊 Summary:
     Users: ${users.length}
     Products: ${products.length}
     Inquiries: ${inquiries.length}
     Colors: ${colors.length}
     Sizes: ${sizes.length}
  
  🔑 Login Credentials:
     Admin:  admin@kickshub.in / admin123
     Dealer: rajesh@kicksfootwear.in / dealer123
     Dealer: priya@stepso.in / dealer123
     Dealer: amit@hammyspot.in / dealer123
  
  🔄 Now REFRESH the page (F5) to see all data!`);
})();
