/* Weekly tracker data for nitori_dashboard.html (tab "Weekly tracker").
   Update once a week: use the form on the tab, press "Download weekly.js", and replace this file
   (GitHub: tracker/weekly.js → Edit or Upload). Plain data only; no code runs from here.

   basket: the fixed list of matched items. Fill nitori / muji / ikea with the exact product
   name or URL in week 1, then keep the same products every week (note any replacement).
   weeks: one entry per check. Prices in yen, tax included, regular online price;
   sale = the Nitori item shows a sale or 値下げ label; stock = Nitori Net shows it in stock.
   site_sale_count / site_sale_disc: items listed on Nitori Net's sale pages and their average
   discount (%); new_count: items on the 新商品 page. Leave a field null if not checked. */
window.NITORI_WEEKLY = {
  basket: [
    {id: 'B01', cat: 'Storage', item: 'Shelf, 3 tiers, about 60 cm wide', nitori: '', muji: '', ikea: ''},
    {id: 'B02', cat: 'Storage', item: 'Fabric storage box, 25-35 cm', nitori: '', muji: '', ikea: ''},
    {id: 'B03', cat: 'Storage', item: 'Plastic drawer case', nitori: '', muji: '', ikea: ''},
    {id: 'B04', cat: 'Bedding', item: 'Duvet, single, all-season', nitori: '', muji: '', ikea: ''},
    {id: 'B05', cat: 'Bedding', item: 'Fitted sheet, single, cotton', nitori: '', muji: '', ikea: ''},
    {id: 'B06', cat: 'Bedding', item: 'Pillow, about 43 x 63 cm', nitori: '', muji: '', ikea: ''},
    {id: 'B07', cat: 'Bath', item: 'Bath towel, cotton, plain', nitori: '', muji: '', ikea: ''},
    {id: 'B08', cat: 'Kitchen', item: 'Frying pan, 26 cm', nitori: '', muji: '', ikea: ''},
    {id: 'B09', cat: 'Kitchen', item: 'Dinner plate, about 25 cm', nitori: '', muji: '', ikea: ''},
    {id: 'B10', cat: 'Kitchen', item: 'Glass food container', nitori: '', muji: '', ikea: ''},
    {id: 'B11', cat: 'Furniture', item: 'Dining chair, wood', nitori: '', muji: '', ikea: ''},
    {id: 'B12', cat: 'Furniture', item: 'Sofa, 2 seats', nitori: '', muji: '', ikea: ''},
    {id: 'B13', cat: 'Furniture', item: 'Low table, about 90 cm', nitori: '', muji: '', ikea: ''},
    {id: 'B14', cat: 'Lighting', item: 'LED desk lamp', nitori: '', muji: '', ikea: ''},
    {id: 'B15', cat: 'Textile', item: 'Curtains, pair, 100 x 200 cm', nitori: '', muji: '', ikea: ''}
  ],
  weeks: [
    /* example of one entry:
    {date: '2026-11-02', prices: {B01: {n: 1990, m: 2990, i: 1999, sale: false, stock: true}},
     site_sale_count: 120, site_sale_disc: 18, new_count: 45, note: ''} */
  ]
};
